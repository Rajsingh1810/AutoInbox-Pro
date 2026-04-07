"""
OpenEnv Inference API for Smart Inbox Assistant
This file must be at repo root for OpenEnv validation
"""

import os
import json
import torch
import numpy as np
from typing import Dict, Any, Optional
from email_env import EmailRLEnv
from stable_baselines3 import PPO


class SmartInboxInference:
    """Inference class for email classification"""
    
    def __init__(self):
        """Initialize inference with trained model"""
        self.env = None
        self.model = None
        self.model_loaded = False
        self.action_names = ["mark_spam", "mark_important", "ignore", "reply"]
        self.action_descriptions = {
            "mark_spam": "🚫 Mark as Spam",
            "mark_important": "⭐ Mark as Important",
            "ignore": "😐 Ignore",
            "reply": "✉️ Reply"
        }
        
        self._load_model()
    
    def _load_model(self):
        """Load the trained PPO model"""
        try:
            # Try multiple paths for model loading
            model_paths = [
                "./models/easy/final_model",
                "models/easy/final_model",
                "/app/models/easy/final_model"
            ]
            
            for model_path in model_paths:
                if os.path.exists(f"{model_path}.zip") or os.path.exists(model_path):
                    print(f"Loading model from: {model_path}")
                    self.model = PPO.load(model_path)
                    self.model_loaded = True
                    print("✅ Model loaded successfully!")
                    return
            
            print("⚠️ No trained model found, will use rule-based fallback")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def _rule_based_fallback(self, email_text: str, difficulty: str) -> Dict[str, Any]:
        """Rule-based fallback when model is not available"""
        email_lower = email_text.lower()
        
        # Spam indicators
        spam_keywords = ['win', 'free', 'money', 'lottery', 'click here', 'urgent', '!!!']
        is_spam = any(keyword in email_lower for keyword in spam_keywords) and '!!!' in email_text
        
        # Important indicators
        important_keywords = ['urgent', 'deadline', 'important', 'critical', 'asap', 'immediate']
        is_important = any(keyword in email_lower for keyword in important_keywords)
        
        if is_spam:
            action = "mark_spam"
            confidence = 0.85
        elif is_important:
            action = "mark_important"
            confidence = 0.75
        else:
            action = "ignore"
            confidence = 0.65
        
        return {
            "action": action,
            "action_emoji": self.action_descriptions[action],
            "confidence": confidence * 100,
            "difficulty": difficulty,
            "model_used": "rule_based_fallback"
        }
    
    def predict(self, email_text: str, difficulty: str = "easy") -> Dict[str, Any]:
        """
        Predict the best action for an email
        
        Args:
            email_text: The email text to classify
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            Dictionary with action, confidence, and metadata
        """
        if not email_text or not email_text.strip():
            return {
                "error": "Email text cannot be empty",
                "status": "error"
            }
        
        try:
            # Initialize environment if not done
            if self.env is None or self.env.difficulty != difficulty:
                self.env = EmailRLEnv(difficulty=difficulty)
            
            # Vectorize email
            obs = self.env._vectorize_email(email_text.strip())
            
            # Get prediction from model
            if self.model_loaded and self.model:
                action, _ = self.model.predict(obs, deterministic=True)
                
                # Calculate confidence using model's policy
                try:
                    obs_tensor = self.model.policy.obs_to_tensor(obs)[0]
                    with torch.no_grad():
                        actions_values = self.model.policy.forward(obs_tensor)
                        probs = torch.nn.functional.softmax(actions_values[0], dim=0)
                        confidence = probs[action].item() * 100
                except Exception as e:
                    print(f"Confidence calculation error: {e}")
                    confidence = 75.0
                
                action_name = self.action_names[action]
                
                return {
                    "action": action_name,
                    "action_emoji": self.action_descriptions[action_name],
                    "confidence": confidence,
                    "difficulty": difficulty,
                    "model_used": "ppo_rl_model",
                    "email_text": email_text.strip()
                }
            else:
                # Fallback to rule-based
                return self._rule_based_fallback(email_text, difficulty)
                
        except Exception as e:
            return {
                "error": f"Prediction failed: {str(e)}",
                "status": "error",
                "email_text": email_text
            }


# Global inference instance
inference = SmartInboxInference()


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    OpenEnv/Hugging Face Inference API handler
    
    Args:
        event: Dictionary with 'inputs' key containing email data
            Example: {"inputs": {"text": "Email content", "difficulty": "easy"}}
    
    Returns:
        Dictionary with prediction results
    """
    try:
        # Extract input
        if isinstance(event, str):
            event = json.loads(event)
        
        inputs = event.get("inputs", event)
        
        if isinstance(inputs, str):
            email_text = inputs
            difficulty = "easy"
        elif isinstance(inputs, dict):
            email_text = inputs.get("text", inputs.get("email", ""))
            difficulty = inputs.get("difficulty", "easy")
        else:
            return {"error": "Invalid input format"}
        
        # Make prediction
        result = inference.predict(email_text, difficulty)
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def reset():
    """
    OpenEnv reset function - reinitializes the inference engine
    This is called by OpenEnv validation system
    """
    global inference
    print("🔄 Resetting inference engine...")
    inference = SmartInboxInference()
    print("✅ Inference engine reset complete")
    return {"status": "success", "message": "Inference engine reset"}


def health_check():
    """Health check endpoint for OpenEnv"""
    return {
        "status": "healthy",
        "model_loaded": inference.model_loaded,
        "service": "smart-inbox-assistant"
    }


if __name__ == "__main__":
    # Test the inference
    test_emails = [
        ("Win money now!!! Click here immediately", "easy"),
        ("URGENT: Submit assignment before midnight", "medium"),
        ("Can we meet tomorrow to discuss the project?", "hard")
    ]
    
    print("\n" + "="*60)
    print("Testing Smart Inbox Inference")
    print("="*60 + "\n")
    
    for email, difficulty in test_emails:
        result = inference.predict(email, difficulty)
        print(f"📧 Email: {email}")
        print(f"   Action: {result.get('action_emoji', result.get('action'))}")
        print(f"   Confidence: {result.get('confidence', 0):.1f}%")
        print(f"   Model: {result.get('model_used')}")
        print()
