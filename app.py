"""
Gradio App for Smart Inbox Assistant
Interactive web interface for Hugging Face Spaces
"""

import gradio as gr
import numpy as np
from email_env import EmailRLEnv
from stable_baselines3 import PPO
import os
import torch

# Try to import inference module for better reliability
try:
    from inference import SmartInboxInference
    inference_engine = SmartInboxInference()
    USE_INFERENCE_ENGINE = True
    print("✅ Using inference engine for predictions")
except Exception as e:
    USE_INFERENCE_ENGINE = False
    print(f"⚠️ Could not load inference engine: {e}")
    print("Falling back to direct model loading")

# Initialize environment
env = EmailRLEnv(difficulty="easy")
action_names = ["mark_spam", "mark_important", "ignore", "reply"]
action_emojis = {
    "mark_spam": "🚫",
    "mark_important": "⭐",
    "ignore": "😐",
    "reply": "✉️"
}

# Try to load trained model (fallback if inference engine fails)
model = None
model_loaded = False

if not USE_INFERENCE_ENGINE:
    try:
        # Check multiple possible paths for the model
        model_paths = [
            "./models/easy/final_model",
            "./model/final_model",
            "models/easy/final_model",
            "/app/models/easy/final_model"
        ]
        
        for model_path in model_paths:
            if os.path.exists(f"{model_path}.zip") or os.path.exists(model_path):
                model = PPO.load(model_path.replace('.zip', ''))
                model_loaded = True
                print(f"✓ Trained model loaded from {model_path}")
                break
        
        if not model_loaded:
            print("⚠ No trained model found, using rule-based fallback")
    except Exception as e:
        print(f"⚠ Could not load model: {e}")


def classify_email(email_text, difficulty="easy"):
    """Classify an email using the RL agent"""

    if not email_text or not email_text.strip():
        return "⚠️ Please enter an email", "", ""

    try:
        # Use inference engine if available
        if USE_INFERENCE_ENGINE:
            result = inference_engine.predict(email_text.strip(), difficulty)
            
            if "error" in result:
                return f"❌ Error: {result['error']}", difficulty, email_text
            
            action_name = result["action"]
            confidence = result["confidence"]
            
        else:
            # Fallback to direct model loading
            global env, model, model_loaded
            
            env = EmailRLEnv(difficulty=difficulty)
            obs = env._vectorize_email(email_text.strip())
            
            if model_loaded and model:
                action, _ = model.predict(obs, deterministic=True)
                action_name = action_names[action]
                
                # Calculate confidence
                try:
                    obs_tensor = model.policy.obs_to_tensor(obs)[0]
                    with torch.no_grad():
                        actions_values = model.policy.forward(obs_tensor)
                        probs = torch.nn.functional.softmax(actions_values[0], dim=0)
                        confidence = probs[action].item() * 100
                except Exception as e:
                    confidence = 75.0
            else:
                # Rule-based fallback
                email_lower = email_text.lower()
                spam_keywords = ['win', 'free', 'money', 'lottery', 'click here', '!!!']
                
                if any(kw in email_lower for kw in spam_keywords):
                    action_name = "mark_spam"
                    confidence = 85.0
                elif any(kw in email_lower for kw in ['urgent', 'deadline', 'important']):
                    action_name = "mark_important"
                    confidence = 75.0
                else:
                    action_name = "ignore"
                    confidence = 65.0

        # Format output
        emoji = action_emojis[action_name]
        result_text = f"{emoji} **Action:** {action_name.replace('_', ' ').title()}"
        result_text += f"\n\n**Confidence:** {confidence:.1f}%"
        result_text += f"\n\n**Mode:** {difficulty}"

        return result_text, difficulty, email_text
        
    except Exception as e:
        return f"❌ Error classifying email: {str(e)}", difficulty, email_text


def show_examples(difficulty):
    """Show example emails for each difficulty"""
    
    examples = {
        "easy": [
            "Win money now!!! Click here immediately",
            "Team meeting scheduled for Monday at 10 AM",
            "FREE iPhone - Click this link now!!!",
            "Your order has been shipped successfully"
        ],
        "medium": [
            "Submit assignment today before midnight",
            "Check out this funny cat video",
            "URGENT: Server maintenance scheduled tonight",
            "Weekend plans discussion thread"
        ],
        "hard": [
            "Can we meet tomorrow to discuss the project?",
            "WIN FREE MONEY NOW!!! Click here immediately!!!",
            "Critical system failure - Need immediate assistance",
            "Would you like to collaborate on this research paper?"
        ]
    }
    
    return examples.get(difficulty, [])


# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📧 Smart Inbox Assistant
    
    An AI-powered email classifier trained with **Reinforcement Learning**!
    
    The agent learns to handle emails like humans do:
    - 🚫 **Mark as Spam**
    - ⭐ **Mark as Important**
    - 😐 **Ignore**
    - ✉️ **Reply**
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            email_input = gr.Textbox(
                label="📧 Enter Email Text",
                placeholder="Paste any email here...",
                lines=4
            )

            difficulty = gr.Radio(
                choices=["easy", "medium", "hard"],
                value="easy",
                label="🎯 Difficulty Level"
            )

            classify_btn = gr.Button("🔍 Classify Email", variant="primary")

        with gr.Column(scale=1):
            output_action = gr.Textbox(label="🤖 AI Decision", lines=5)
            output_difficulty = gr.Textbox(label="📊 Mode", value="easy", interactive=False, visible=False)
            output_email = gr.Textbox(label="📝 Email", interactive=False, visible=False)
    
    gr.Markdown("---")
    gr.Markdown("### 💡 Try These Examples:")

    examples = gr.Dataframe(
        headers=["Example Emails"],
        wrap=True,
        interactive=False
    )

    def update_examples(difficulty):
        ex = show_examples(difficulty)
        return [[ex] for ex in ex]

    difficulty.change(fn=update_examples, inputs=difficulty, outputs=examples)
    
    # Update examples on load
    demo.load(fn=lambda: update_examples("easy"), inputs=None, outputs=examples)

    classify_btn.click(
        fn=classify_email,
        inputs=[email_input, difficulty],
        outputs=[output_action, output_difficulty, output_email]
    )

    email_input.submit(
        fn=classify_email,
        inputs=[email_input, difficulty],
        outputs=[output_action, output_difficulty, output_email]
    )

    gr.Markdown("""
    ---
    **🧠 How it works:** This uses a PPO (Proximal Policy Optimization) RL agent
    trained on email classification tasks. The agent learns through trial and error
    to maximize rewards for correct actions.

    **📚 Learn more:** Check out the [GitHub Repository](https://github.com) for code and training scripts!
    """)

if __name__ == "__main__":
    # Start FastAPI server for OpenEnv compatibility
    import uvicorn
    import threading
    
    # Gradio runs in background
    gradio_thread = threading.Thread(target=lambda: demo.launch(server_name="0.0.0.0", server_port=7861, quiet=True), daemon=True)
    gradio_thread.start()
    
    # Import and run API server
    from server import app as api_app
    print("🚀 Starting API Server on port 7860...")
    uvicorn.run(api_app, host="0.0.0.0", port=7860)
