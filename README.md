# Smart Inbox Assistant - RL Environment

An AI-powered email classification system using Reinforcement Learning that learns to handle emails like humans do daily.

## 🎯 What This Does

This environment trains an AI agent to:
- **Read emails** and understand their meaning
- **Take correct actions**: Mark as spam, mark important, ignore, or reply
- **Learn from feedback** through rewards system

## 📋 Features

✅ **Three Difficulty Levels:**
- 🟢 **Easy**: Spam detection
- 🟡 **Medium**: Important email detection
- 🔴 **Hard**: Reply suggestion

✅ **Real RL Environment:**
- State: Email text (TF-IDF vectorized)
- Action: 4 choices (spam/important/ignore/reply)
- Reward: 1.0 (correct), 0.5 (partial), 0.0 (wrong)
- Episode: Ends after 1 step

✅ **Complete Training Pipeline:**
- PPO algorithm from Stable-Baselines3
- Evaluation callbacks
- Model saving/loading
- Interactive demo mode

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd smart-inbox-rl
pip install -r requirements.txt
```

### 2. Train the Agent

```bash
python train.py
```

This will:
- Train models for all 3 difficulty levels
- Save trained models to `./models/`
- Display evaluation results

### 3. Test the Model

```bash
python demo.py
```

### 4. Interactive Mode

```bash
python demo.py interactive
```

Enter your own emails and see how the AI classifies them!

## 📁 Project Structure

```
smart-inbox-rl/
├── email_env.py          # Custom RL environment
├── train.py              # Training script
├── demo.py               # Demo and testing
├── requirements.txt      # Dependencies
├── models/               # Saved models (after training)
│   ├── easy/
│   ├── medium/
│   └── hard/
└── logs/                 # Training logs
```

## 🧠 How It Works

### RL Loop

```
Email (State)
    ↓
Agent chooses Action
    ↓
Environment gives Reward
    ↓
Agent learns from Reward
    ↓
Repeat...
```

### Actions

| Action | Meaning |
|--------|---------|
| 0 | Mark as Spam |
| 1 | Mark as Important |
| 2 | Ignore |
| 3 | Reply |

### Reward System

| Situation | Reward |
|-----------|--------|
| Correct action | 1.0 |
| Partially correct | 0.5 |
| Wrong action | 0.0 |

## 🛠️ Customization

### Add More Emails

Edit `email_env.py` and add emails to:
- `EASY_EMAILS` dict
- `MEDIUM_EMAILS` dict
- `HARD_EMAILS` dict

### Change Training Parameters

In `train.py`, modify:
```python
model = PPO(
    "MlpPolicy",
    vec_env,
    learning_rate=3e-4,    # Learning rate
    n_steps=128,           # Steps per update
    n_epochs=10,           # Epochs per update
    ...
)
```

### Use Different Algorithm

Replace PPO with DQN, A2C, etc.:
```python
from stable_baselines3 import DQN, A2C
model = DQN("MlpPolicy", vec_env)
```

## 📊 Example Output

```
============================================================
Testing Trained Model - EASY Level
============================================================

✅ Email: Win lottery now!!! Click here
   Expected: mark_spam
   Predicted: mark_spam

❌ Email: Team meeting Monday 10 AM
   Expected: ignore
   Predicted: mark_spam

============================================================
📊 Results: 8/10 correct
   Accuracy: 80.0%
============================================================
```

## 🎓 Learning Objectives

This project teaches:
- Reinforcement Learning fundamentals
- Custom Gym environments
- State/Action/Reward design
- Text vectorization (TF-IDF)
- PPO algorithm training
- Model evaluation

## 📝 Notes

- **Training Time**: ~5-10 minutes for basic performance
- **Better Performance**: Increase `total_timesteps` in `train.py`
- **TensorBoard**: View training logs with `tensorboard --logdir ./logs/`

## 🐛 Troubleshooting

**Issue**: Module not found error
```bash
pip install -r requirements.txt
```

**Issue**: Low accuracy
- Increase training timesteps
- Add more diverse email data
- Adjust hyperparameters

## 📄 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Add more email examples, implement new difficulty levels, or try different RL algorithms!
