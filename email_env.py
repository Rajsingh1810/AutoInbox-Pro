"""
Smart Inbox Assistant - Reinforcement Learning Environment
Email classification environment with 3 difficulty levels:
- Easy: Spam detection
- Medium: Important email detection  
- Hard: Reply suggestion
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
import json


class EmailRLEnv(gym.Env):
    """
    Custom RL Environment for email classification
    
    Actions:
    0: mark_spam
    1: mark_important
    2: ignore
    3: reply
    
    Reward:
    - Correct action: 1.0
    - Partially correct: 0.5
    - Wrong action: 0.0
    """
    
    metadata = {'render_modes': ['human']}
    
    # Email datasets for each difficulty level
    EASY_EMAILS = {
        "spam": [
            "Win money now!!! Click here immediately",
            "Congratulations! You won lottery worth $1000000",
            "FREE iPhone - Click this link now!!!",
            "Make $5000 per week working from home",
            "URGENT: Verify your bank account details now",
            "You have been selected for a free vacation",
            "Earn cash fast with this one simple trick",
            "LIMITED OFFER: Buy now and save 99%",
            "Your account will be suspended - Click here",
            "Claim your prize before it expires today"
        ],
        "not_spam": [
            "Team meeting scheduled for Monday at 10 AM",
            "Your order has been shipped successfully",
            "Project deadline extended to next Friday",
            "Monthly newsletter - Company updates",
            "Reminder: Dentist appointment tomorrow",
            "Your subscription renewal confirmation",
            "Class notes from yesterday's lecture",
            "Weather update for this weekend",
            "Recipe sharing for dinner party",
            "Book club meeting notes and discussion"
        ]
    }
    
    MEDIUM_EMAILS = {
        "important": [
            "Submit assignment today before midnight",
            "URGENT: Server maintenance scheduled tonight",
            "Interview confirmation - Tomorrow 2 PM",
            "Payment due date is approaching fast",
            "Critical security update required immediately",
            "Final year project submission deadline",
            "Exam schedule released - Check dates",
            "Important: Policy changes effective next month",
            "Scholarship application closing soon",
            "Mandatory training session this week"
        ],
        "not_important": [
            "Check out this funny cat video",
            "Weekend plans discussion thread",
            "New restaurant opening in town",
            "Sports update from last night game",
            "Celebrity gossip and news roundup",
            "Fun quiz: Which character are you?",
            "Random meme collection for laughs",
            "Casual chat group invitation",
            "Entertainment blog weekly digest",
            "Photo album from office party"
        ]
    }
    
    HARD_EMAILS = {
        "meeting_request": {
            "email": "Can we meet tomorrow to discuss the project?",
            "correct_action": 3,  # reply
            "good_reply": "Yes, I am available tomorrow. What time works for you?"
        },
        "question": {
            "email": "What is the deadline for this task?",
            "correct_action": 3,
            "good_reply": "The deadline is next Friday. Let me know if you need more details."
        },
        "spam_obvious": {
            "email": "WIN FREE MONEY NOW!!! Click here immediately!!!",
            "correct_action": 0,  # mark_spam
            "good_reply": None
        },
        "important_urgent": {
            "email": "Critical system failure - Need immediate assistance",
            "correct_action": 1,  # mark_important
            "good_reply": None
        },
        "informational": {
            "email": "Office will be closed on Friday for maintenance",
            "correct_action": 2,  # ignore
            "good_reply": None
        },
        "collaboration": {
            "email": "Would you like to collaborate on this research paper?",
            "correct_action": 3,
            "good_reply": "I'd be interested. Let's discuss the scope and timeline."
        },
        "feedback_request": {
            "email": "Can you review my code and provide feedback?",
            "correct_action": 3,
            "good_reply": "Sure, I'll review it and get back to you by tomorrow."
        },
        "newsletter": {
            "email": "Weekly digest: Top 10 articles you might have missed",
            "correct_action": 2,
            "good_reply": None
        }
    }
    
    def __init__(self, difficulty: str = "easy", render_mode: Optional[str] = None):
        super().__init__()
        
        assert difficulty in ["easy", "medium", "hard"], "Difficulty must be easy, medium, or hard"
        self.difficulty = difficulty
        
        # Action space: 0=spam, 1=important, 2=ignore, 3=reply
        self.action_space = spaces.Discrete(4)
        
        # Observation space: TF-IDF vectorized email text (max 100 features for simplicity)
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        
        # Fit vectorizer on all email data
        all_emails = self._get_all_emails()
        self.vectorizer.fit(all_emails)
        
        # Observation space dimension
        obs_dim = len(self.vectorizer.get_feature_names_out())
        self.observation_space = spaces.Box(
            low=0.0, 
            high=1.0, 
            shape=(obs_dim,), 
            dtype=np.float32
        )
        
        self.current_email = None
        self.current_email_text = ""
        self.correct_action = None
        self.render_mode = render_mode
        
    def _get_all_emails(self) -> list:
        """Get all emails from all difficulty levels for vectorizer fitting"""
        all_emails = []
        
        # Easy emails
        for emails in self.EASY_EMAILS.values():
            all_emails.extend(emails)
            
        # Medium emails
        for emails in self.MEDIUM_EMAILS.values():
            all_emails.extend(emails)
            
        # Hard emails
        for email_data in self.HARD_EMAILS.values():
            all_emails.append(email_data["email"])
            
        return all_emails
    
    def _get_email_dataset(self) -> Dict:
        """Get email dataset based on difficulty"""
        if self.difficulty == "easy":
            return self.EASY_EMAILS
        elif self.difficulty == "medium":
            return self.MEDIUM_EMAILS
        else:
            return self.HARD_EMAILS
    
    def reset(
        self, 
        seed: Optional[int] = None, 
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset the environment and return a new email"""
        super().reset(seed=seed)
        
        dataset = self._get_email_dataset()
        
        if self.difficulty in ["easy", "medium"]:
            # Randomly select category (spam/not_spam or important/not_important)
            categories = list(dataset.keys())
            category = self.np_random.choice(categories)
            
            # Randomly select email from category
            email_idx = self.np_random.integers(0, len(dataset[category]))
            self.current_email_text = dataset[category][email_idx]
            
            # Determine correct action
            if self.difficulty == "easy":
                self.correct_action = 0 if category == "spam" else 2  # spam or ignore
            else:  # medium
                self.correct_action = 1 if category == "important" else 2  # important or ignore
                
        else:  # hard
            # Select random hard email
            email_key = self.np_random.choice(list(dataset.keys()))
            email_data = dataset[email_key]
            self.current_email_text = email_data["email"]
            self.correct_action = email_data["correct_action"]
        
        # Vectorize email
        obs = self._vectorize_email(self.current_email_text)
        
        # Get correct label for info
        if self.difficulty in ["easy", "medium"]:
            category_name = [k for k, v in dataset.items() 
                           if self.current_email_text in v][0]
        else:
            category_name = [k for k, v in dataset.items() 
                           if v["email"] == self.current_email_text][0]
        
        return obs, {"email_text": self.current_email_text, 
                     "correct_action": self.correct_action,
                     "category": category_name}
    
    def _vectorize_email(self, text: str) -> np.ndarray:
        """Convert email text to TF-IDF vector"""
        vector = self.vectorizer.transform([text]).toarray()[0]
        return vector.astype(np.float32)
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """Execute one step in the environment"""
        
        # Calculate reward
        reward = self._calculate_reward(action)
        
        # Episode always ends after 1 step (simple version)
        terminated = True
        truncated = False
        
        # Info dictionary
        info = {
            "email_text": self.current_email_text,
            "action_taken": action,
            "correct_action": self.correct_action,
            "action_names": ["mark_spam", "mark_important", "ignore", "reply"]
        }
        
        # Empty observation for next state (episode ends)
        obs = np.zeros(self.observation_space.shape[0], dtype=np.float32)
        
        return obs, reward, terminated, truncated, info
    
    def _calculate_reward(self, action: int) -> float:
        """Calculate reward based on action correctness"""
        if action == self.correct_action:
            return 1.0
        elif self._is_partially_correct(action, self.correct_action):
            return 0.5
        else:
            return 0.0
    
    def _is_partially_correct(self, action: int, correct: int) -> bool:
        """Define partial correctness logic"""
        # For easy/medium: treating spam as unimportant or vice versa is partially correct
        if self.difficulty in ["easy", "medium"]:
            # Both are non-reply actions
            return action in [0, 1, 2] and correct in [0, 1, 2] and action != correct
        else:
            # For hard: reply vs non-reply is the main distinction
            return (action == 3 and correct in [0, 1, 2]) or \
                   (action in [0, 1, 2] and correct == 3)
    
    def render(self):
        """Render the current state"""
        if self.render_mode == "human":
            action_names = ["mark_spam", "mark_important", "ignore", "reply"]
            print(f"\n{'='*50}")
            print(f"Email: {self.current_email_text}")
            print(f"Correct Action: {action_names[self.correct_action]}")
            print(f"{'='*50}")
    
    def close(self):
        """Clean up resources"""
        pass


if __name__ == "__main__":
    # Test the environment
    print("Testing Easy Level (Spam Detection):")
    env = EmailRLEnv(difficulty="easy")
    obs, info = env.reset()
    print(f"Email: {info['email_text']}")
    print(f"Correct Action: {info['correct_action']}")
    
    # Take random action
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Action taken: {action}")
    print(f"Reward: {reward}")
    print(f"Episode ended: {terminated}")
    
    print("\n" + "="*50)
    print("Testing Medium Level (Important Email Detection):")
    env = EmailRLEnv(difficulty="medium")
    obs, info = env.reset()
    print(f"Email: {info['email_text']}")
    print(f"Correct Action: {info['correct_action']}")
    
    print("\n" + "="*50)
    print("Testing Hard Level (Reply Suggestion):")
    env = EmailRLEnv(difficulty="hard")
    obs, info = env.reset()
    print(f"Email: {info['email_text']}")
    print(f"Correct Action: {info['correct_action']}")
