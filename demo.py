"""
Interactive demonstration script for Smart Inbox Assistant
Test the trained RL agent with custom emails
"""

from email_env import EmailRLEnv
from stable_baselines3 import PPO
import numpy as np


def demonstrate_with_custom_emails(model_path=None, difficulty="easy"):
    """Test agent with custom email examples"""
    
    print(f"\n{'='*60}")
    print(f"Smart Inbox Assistant Demo - {difficulty.upper()} Level")
    print(f"{'='*60}\n")
    
    # Load model if provided
    model = None
    if model_path:
        try:
            model = PPO.load(model_path)
            print("✓ Trained model loaded\n")
        except:
            print("⚠ Could not load model, using random policy\n")
    
    # Custom test emails
    test_emails = {
        "easy": [
            ("Win lottery now!!! Click here", 0),  # spam
            ("Team meeting Monday 10 AM", 2),       # ignore
            ("FREE iPhone - Act now!!!", 0),        # spam
            ("Project deadline next Friday", 2),    # ignore
        ],
        "medium": [
            ("Submit assignment today before midnight", 1),  # important
            ("Funny cat video link", 2),                     # ignore
            ("URGENT: Server maintenance tonight", 1),       # important
            ("Weekend plans discussion", 2),                 # ignore
        ],
        "hard": [
            ("Can we meet tomorrow to discuss?", 3),         # reply
            ("WIN FREE MONEY NOW!!!", 0),                    # spam
            ("Critical system failure - Help needed", 1),    # important
            ("Office closed Friday for maintenance", 2),     # ignore
        ]
    }
    
    env = EmailRLEnv(difficulty=difficulty)
    action_names = ["mark_spam", "mark_important", "ignore", "reply"]
    
    print("Testing Custom Emails:\n")
    
    correct_count = 0
    total_count = len(test_emails[difficulty])
    
    for email_text, expected_action in test_emails[difficulty]:
        # Vectorize email
        obs = env._vectorize_email(email_text)
        
        # Get action from model or random
        if model:
            action, _ = model.predict(obs, deterministic=True)
        else:
            action = env.action_space.sample()
        
        # Determine correct action for this email
        if difficulty in ["easy", "medium"]:
            # For easy/medium, we need to infer correct action
            if difficulty == "easy":
                correct_action = 0 if expected_action == 0 else 2
            else:
                correct_action = 1 if expected_action == 1 else 2
        else:
            correct_action = expected_action
        
        # Check if correct
        is_correct = (action == correct_action)
        if is_correct:
            correct_count += 1
        
        # Display results
        emoji = "✅" if is_correct else "❌"
        print(f"{emoji} Email: {email_text}")
        print(f"   Expected: {action_names[correct_action]}")
        print(f"   Predicted: {action_names[action]}")
        print()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Results: {correct_count}/{total_count} correct")
    print(f"   Accuracy: {(correct_count/total_count * 100):.1f}%")
    print(f"{'='*60}\n")


def interactive_demo(model_path=None):
    """Interactive mode where user can input custom emails"""
    
    print(f"\n{'='*60}")
    print(f"Interactive Smart Inbox Assistant")
    print(f"{'='*60}\n")
    
    # Load model if provided
    model = None
    if model_path:
        try:
            model = PPO.load(model_path)
            print("✓ Trained model loaded\n")
        except:
            print("⚠ Could not load model, using random policy\n")
    
    env = EmailRLEnv(difficulty="easy")
    action_names = ["mark_spam", "mark_important", "ignore", "reply"]
    
    print("Enter emails to classify (type 'quit' to exit):\n")
    
    while True:
        try:
            email = input("📧 Email: ").strip()
            
            if email.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not email:
                continue
            
            # Vectorize email
            obs = env._vectorize_email(email)
            
            # Get action
            if model:
                action, _ = model.predict(obs, deterministic=True)
            else:
                action = env.action_space.sample()
            
            # Display result
            print(f"   → Action: {action_names[action]}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"   ⚠ Error: {e}\n")


if __name__ == "__main__":
    import sys
    
    # Check if interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        model_path = sys.argv[2] if len(sys.argv) > 2 else None
        interactive_demo(model_path)
    else:
        # Demo all difficulty levels
        for difficulty in ["easy", "medium", "hard"]:
            model_path = f"./models/{difficulty}/final_model"
            demonstrate_with_custom_emails(model_path, difficulty)
