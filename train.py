"""
Training script for Smart Inbox Assistant RL Environment
Uses PPO (Proximal Policy Optimization) algorithm from Stable-Baselines3
"""

import os
import resend
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback
from email_env import EmailRLEnv
import gymnasium as gym

# Configure Resend API
resend.api_key = "re_Pi98pBtu_GNBHhSLidPZrLqmPmhDdvduX"


def send_training_email(difficulty, mean_reward, std_reward, accuracy):
    """Send email notification when training completes"""
    try:
        email_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #4CAF50;">🎉 Smart Inbox Assistant Training Complete!</h2>
            <p>Training has been completed for the <strong>{difficulty.upper()}</strong> difficulty level.</p>
            
            <h3 style="color: #2196F3;">📊 Performance Metrics:</h3>
            <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Difficulty Level</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{difficulty.upper()}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Mean Reward</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{mean_reward:.2f}</td>
                </tr>
                <tr style="background-color: #f2f2f2;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Standard Deviation</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">±{std_reward:.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Accuracy</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd; color: #4CAF50; font-weight: bold;">{accuracy:.1f}%</td>
                </tr>
            </table>
            
            <p style="margin-top: 20px; color: #666;">The trained model has been saved to <code>./models/{difficulty}/final_model</code></p>
            
            <hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
            <p style="color: #999; font-size: 12px;">Smart Inbox Assistant - Reinforcement Learning System</p>
        </body>
        </html>
        """
        
        r = resend.Emails.send({
            "from": "Smart Inbox <onboarding@resend.dev>",
            "to": "2004rajraslpur@gmail.com",
            "subject": f"✅ Training Complete - {difficulty.upper()} Level ({accuracy:.1f}% Accuracy)",
            "html": email_html
        })
        
        print(f"📧 Training completion email sent successfully (ID: {r['id']})")
        return r
    except Exception as e:
        print(f"⚠️  Failed to send training email: {str(e)}")
        return None


def train_model(difficulty="easy", total_timesteps=50000, save_dir="./models"):
    """
    Train RL agent on specified difficulty level
    
    Args:
        difficulty: "easy", "medium", or "hard"
        total_timesteps: Number of training steps
        save_dir: Directory to save models
    """
    
    print(f"\n{'='*60}")
    print(f"Training Smart Inbox Assistant - {difficulty.upper()} Level")
    print(f"{'='*60}\n")
    
    # Create vectorized environment (parallel environments for faster training)
    vec_env = make_vec_env(
        lambda: EmailRLEnv(difficulty=difficulty), 
        n_envs=4
    )
    
    # Create evaluation environment
    eval_env = EmailRLEnv(difficulty=difficulty)
    
    # Create callback to evaluate during training
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=f"{save_dir}/{difficulty}/",
        log_path=f"{save_dir}/{difficulty}/logs/",
        eval_freq=500,
        n_eval_episodes=10,
        deterministic=True,
        verbose=1
    )
    
    # Initialize PPO model
    model = PPO(
        "MlpPolicy",
        vec_env,
        learning_rate=3e-4,
        n_steps=128,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,  # Encourage exploration
        verbose=1,
        tensorboard_log=f"./logs/{difficulty}/"
    )
    
    # Train the model
    model.learn(
        total_timesteps=total_timesteps,
        callback=eval_callback,
        progress_bar=True
    )
    
    # Save final model
    os.makedirs(f"{save_dir}/{difficulty}", exist_ok=True)
    model.save(f"{save_dir}/{difficulty}/final_model")
    
    print(f"\n✓ Model saved to {save_dir}/{difficulty}/final_model")
    
    # Evaluate final model
    mean_reward, std_reward = evaluate_policy(model, eval_env, n_eval_episodes=20)
    accuracy = mean_reward * 100
    print(f"\n📊 Final Evaluation:")
    print(f"   Mean Reward: {mean_reward:.2f} ± {std_reward:.2f}")
    print(f"   Accuracy: {accuracy:.1f}%\n")

    # Send email notification
    send_training_email(difficulty, mean_reward, std_reward, accuracy)

    return model


def test_trained_model(difficulty="easy", model_path="./models/easy/final_model"):
    """Test a trained model with detailed output"""
    
    print(f"\n{'='*60}")
    print(f"Testing Trained Model - {difficulty.upper()} Level")
    print(f"{'='*60}\n")
    
    # Load trained model
    model = PPO.load(model_path)
    
    # Create environment
    env = EmailRLEnv(difficulty=difficulty, render_mode="human")
    
    # Test on multiple episodes
    num_episodes = 10
    correct_count = 0
    total_reward = 0
    
    action_names = ["mark_spam", "mark_important", "ignore", "reply"]
    
    for i in range(num_episodes):
        obs, info = env.reset()
        env.render()
        
        # Predict action
        action, _ = model.predict(obs, deterministic=True)
        
        # Step environment
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Display results
        print(f"Agent Action: {action_names[info['action_taken']]}")
        print(f"Correct Action: {action_names[info['correct_action']]}")
        print(f"Reward: {reward}")
        print(f"{'='*50}")
        
        if reward == 1.0:
            correct_count += 1
        total_reward += reward
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Correct: {correct_count}/{num_episodes}")
    print(f"   Accuracy: {(correct_count/num_episodes * 100):.1f}%")
    print(f"   Average Reward: {total_reward/num_episodes:.2f}\n")


if __name__ == "__main__":
    # Train on all difficulty levels
    difficulties = ["easy", "medium", "hard"]
    
    for difficulty in difficulties:
        # Train model
        model = train_model(
            difficulty=difficulty,
            total_timesteps=10000,  # Increase for better performance
            save_dir="./models"
        )
        
        # Test the trained model
        test_trained_model(
            difficulty=difficulty,
            model_path=f"./models/{difficulty}/final_model"
        )
    
    print("\n✅ Training complete for all difficulty levels!")
