"""
OpenEnv Inference Script for Smart Inbox Assistant
Must use OpenAI Client and emit [START], [STEP], [END] logs
"""

import os
import json
import time
from typing import Dict, Any, List
from openai import OpenAI
from email_env import EmailRLEnv
from openenv_env import SmartInboxEnv, Observation, State, GraderResult


# Environment variables (MANDATORY per requirements)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "")


def get_llm_client() -> OpenAI:
    """Initialize OpenAI client using environment variables"""
    return OpenAI(
        api_key=HF_TOKEN,
        base_url=API_BASE_URL
    )


def classify_email_with_llm(email_text: str, difficulty: str) -> int:
    """
    Use LLM to classify email
    Returns action: 0=spam, 1=important, 2=ignore, 3=reply
    """
    client = get_llm_client()
    
    prompt = f"""Classify this email into one of 4 actions:
0 = mark_spam (obvious spam, scams, promotions)
1 = mark_important (urgent, deadlines, critical info)
2 = ignore (informational, newsletters, casual)
3 = reply (questions, meeting requests, collaboration)

Difficulty: {difficulty}
Email: {email_text}

Return ONLY the action number (0, 1, 2, or 3)."""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an email classification assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=10
        )
        
        action = int(response.choices[0].message.content.strip())
        return max(0, min(3, action))
    except Exception as e:
        print(f"LLM error: {e}, using fallback")
        return 2  # Fallback to ignore


def run_evaluation():
    """
    Run evaluation on all difficulty levels
    Emits [START], [STEP], [END] structured logs
    """
    env = SmartInboxEnv()
    difficulties = ["easy", "medium", "hard"]
    
    print(f"[START] evaluation model={MODEL_NAME} difficulties={len(difficulties)}")
    
    all_results = []
    
    for difficulty in difficulties:
        print(f"[START] difficulty={difficulty}")
        
        # Run multiple episodes per difficulty
        env.reset(difficulty=difficulty)
        episode_reward = 0.0
        episodes = 5
        
        for episode in range(episodes):
            obs = env.reset(difficulty=difficulty)
            
            # Get action from LLM
            action = classify_email_with_llm(obs.email_text, difficulty)
            
            # Take step
            state, reward, done = env.step(action)
            
            episode_reward += reward
            
            print(f"[STEP] difficulty={difficulty} episode={episode} action={action} "
                  f"correct={obs.correct_action if hasattr(obs, 'correct_action') else state.correct_action} "
                  f"reward={reward} done={done}")
        
        # Calculate score for this difficulty
        score = episode_reward / episodes
        print(f"[END] difficulty={difficulty} episodes={episodes} "
              f"total_reward={episode_reward} score={score:.2f}")
        
        all_results.append({
            "difficulty": difficulty,
            "episodes": episodes,
            "total_reward": episode_reward,
            "score": score
        })
    
    # Final summary
    avg_score = sum(r["score"] for r in all_results) / len(all_results)
    print(f"[END] evaluation_complete avg_score={avg_score:.2f} "
          f"model={MODEL_NAME}")
    
    return all_results, avg_score


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hugging Face / OpenEnv inference handler
    """
    try:
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
        
        # Classify email
        action = classify_email_with_llm(email_text, difficulty)
        action_names = ["mark_spam", "mark_important", "ignore", "reply"]
        
        return {
            "status": "success",
            "result": {
                "action": action,
                "action_name": action_names[action],
                "difficulty": difficulty,
                "email_text": email_text
            }
        }
        
    except Exception as e:
        return {"error": str(e)}


def reset():
    """OpenEnv reset endpoint"""
    return {"status": "success", "message": "Inference engine reset"}


def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "api_url": API_BASE_URL
    }


if __name__ == "__main__":
    print("="*60)
    print("Smart Inbox Assistant - OpenEnv Inference")
    print(f"Model: {MODEL_NAME}")
    print(f"API: {API_BASE_URL}")
    print("="*60)
    
    results, avg_score = run_evaluation()
    
    print("\n" + "="*60)
    print("Results Summary:")
    for r in results:
        print(f"  {r['difficulty']}: score={r['score']:.2f} "
              f"episodes={r['episodes']}")
    print(f"  Average Score: {avg_score:.2f}")
    print("="*60)
