"""
Gradio App for Smart Inbox Assistant
Interactive web interface for Hugging Face Spaces
"""

import gradio as gr
import numpy as np
from email_env import EmailRLEnv
from stable_baselines3 import PPO
import os

# Initialize environment
env = EmailRLEnv(difficulty="easy")
action_names = ["mark_spam", "mark_important", "ignore", "reply"]
action_emojis = {
    "mark_spam": "🚫",
    "mark_important": "⭐",
    "ignore": "😐",
    "reply": "✉️"
}

# Try to load trained model
model = None
model_loaded = False

try:
    # Check if model exists
    if os.path.exists("./model/final_model.zip"):
        model = PPO.load("./model/final_model")
        model_loaded = True
        print("✓ Trained model loaded")
    else:
        print("⚠ No trained model found, using random policy")
except Exception as e:
    print(f"⚠ Could not load model: {e}")


def classify_email(email_text, difficulty="easy"):
    """Classify an email using the RL agent"""
    
    if not email_text or not email_text.strip():
        return "⚠️ Please enter an email", "", ""
    
    # Update environment difficulty
    global env
    env = EmailRLEnv(difficulty=difficulty)
    
    # Vectorize email
    obs = env._vectorize_email(email_text.strip())
    
    # Get action from model or random
    if model_loaded and model:
        action, _ = model.predict(obs, deterministic=True)
    else:
        action = env.action_space.sample()
    
    action_name = action_names[action]
    emoji = action_emojis[action_name]
    
    # Create result
    result = f"{emoji} **Action:** {action_name.replace('_', ' ').title()}"
    
    # Confidence (if using model)
    if model_loaded and model:
        # Get action probabilities
        obs_tensor = model.policy.obs_to_tensor(obs)[0]
        with model.policy.th.inference_mode():
            actions_values = model.policy.forward(obs_tensor)
            # Softmax to get probabilities
            import torch
            probs = torch.nn.functional.softmax(actions_values[0], dim=0)
            confidence = probs[action].item() * 100
            result += f"\n\n**Confidence:** {confidence:.1f}%"
    
    return result, difficulty, email_text


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
            output_action = gr.Textbox(label="🤖 AI Decision", lines=3)
            output_difficulty = gr.Textbox(label="📊 Mode", interactive=False)
            output_email = gr.Textbox(label="📝 Email", interactive=False)
    
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

# Update examples on load
demo.load(fn=lambda: update_examples("easy"), inputs=None, outputs=examples)

if __name__ == "__main__":
    demo.launch()
