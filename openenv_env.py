"""
OpenEnv-compatible environment for Smart Inbox Assistant
Implements step()/reset()/state() API with typed models
"""

import os
import json
import time
from typing import Dict, Any, Optional, Tuple, List
from pydantic import BaseModel, Field
from email_env import EmailRLEnv
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# Typed Models for OpenEnv spec
class Observation(BaseModel):
    """Environment observation"""
    email_text: str = Field(..., description="The email text to classify")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    vectorized: Optional[List[float]] = Field(None, description="TF-IDF vectorized email")


class Action(BaseModel):
    """Environment action"""
    action: int = Field(..., description="Action: 0=spam, 1=important, 2=ignore, 3=reply")
    action_name: str = Field(..., description="Action name")


class State(BaseModel):
    """Environment state"""
    done: bool = Field(..., description="Whether episode is complete")
    reward: float = Field(..., description="Reward for the action taken")
    score: float = Field(..., description="Normalized score 0.0-1.0")
    email_text: str = Field(..., description="Current email")
    correct_action: int = Field(..., description="Expected action")
    difficulty: str = Field(..., description="Current difficulty")


class GraderResult(BaseModel):
    """Grader evaluation result"""
    score: float = Field(..., ge=0.0, le=1.0, description="Score between 0.0 and 1.0")
    feedback: str = Field(..., description="Feedback on performance")
    passed: bool = Field(..., description="Whether task passed")


class SmartInboxEnv:
    """
    OpenEnv-compatible environment for email classification
    
    Actions:
        0: mark_spam
        1: mark_important
        2: ignore
        3: reply
    
    Reward: 1.0 (correct), 0.5 (partial), 0.0 (wrong)
    """
    
    def __init__(self):
        self.env = None
        self.current_difficulty = "easy"
        self.current_observation = None
        self.correct_action = None
        self.episode_count = 0
        self.total_reward = 0.0
        
    def reset(self, difficulty: str = "easy") -> Observation:
        """
        Reset environment and return initial observation
        
        Args:
            difficulty: "easy", "medium", or "hard"
        
        Returns:
            Observation object with email text
        """
        self.current_difficulty = difficulty
        self.env = EmailRLEnv(difficulty=difficulty)
        
        obs, info = self.env.reset()
        self.current_observation = obs
        self.correct_action = info["correct_action"]
        self.episode_count += 1
        
        print(f"[START] difficulty={difficulty} episode={self.episode_count}")
        
        return Observation(
            email_text=info["email_text"],
            difficulty=difficulty,
            vectorized=obs.tolist()
        )
    
    def step(self, action: int) -> Tuple[State, float, bool]:
        """
        Take a step in the environment
        
        Args:
            action: Action to take (0-3)
        
        Returns:
            (state, reward, done)
        """
        if self.env is None:
            raise ValueError("Environment not initialized. Call reset() first.")
        
        obs, reward, terminated, truncated, info = self.env.step(action)
        
        done = terminated or truncated
        self.total_reward += reward
        
        state = State(
            done=done,
            reward=reward,
            score=reward,  # Reward is already 0.0-1.0
            email_text=info["email_text"],
            correct_action=info["correct_action"],
            difficulty=self.current_difficulty
        )
        
        print(f"[STEP] action={action} reward={reward} done={done}")
        
        return state, reward, done
    
    def state(self) -> State:
        """
        Get current environment state
        
        Returns:
            Current State object
        """
        if self.env is None:
            return State(
                done=True,
                reward=0.0,
                score=0.0,
                email_text="",
                correct_action=0,
                difficulty=self.current_difficulty
            )
        
        return State(
            done=False,
            reward=self.total_reward / max(self.episode_count, 1),
            score=self.total_reward / max(self.episode_count, 1),
            email_text=self.env.current_email_text if self.env else "",
            correct_action=self.correct_action if self.correct_action else 0,
            difficulty=self.current_difficulty
        )
    
    def grade_easy(self, action: int, correct: int) -> GraderResult:
        """Grader for easy difficulty - spam detection"""
        score = 1.0 if action == correct else 0.0
        passed = action == correct
        feedback = "Correct spam detection" if passed else "Incorrect spam detection"
        return GraderResult(score=score, feedback=feedback, passed=passed)
    
    def grade_medium(self, action: int, correct: int) -> GraderResult:
        """Grader for medium difficulty - important email detection"""
        score = 1.0 if action == correct else 0.0
        passed = action == correct
        feedback = "Correct important detection" if passed else "Incorrect important detection"
        return GraderResult(score=score, feedback=feedback, passed=passed)
    
    def grade_hard(self, action: int, correct: int) -> GraderResult:
        """Grader for hard difficulty - reply suggestion"""
        score = 1.0 if action == correct else 0.0
        passed = action == correct
        feedback = "Correct reply detection" if passed else "Incorrect reply detection"
        return GraderResult(score=score, feedback=feedback, passed=passed)
