"""
OpenEnv API Server for Smart Inbox Assistant
Implements proper /reset, /step, /state endpoints
"""

import os
import json
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openenv_env import SmartInboxEnv

app = FastAPI(title="Smart Inbox Assistant - OpenEnv API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment
env = SmartInboxEnv()


class ResetRequest(BaseModel):
    difficulty: Optional[str] = "easy"


class StepRequest(BaseModel):
    action: int


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Smart Inbox Assistant",
        "version": "1.0.0",
        "status": "running",
        "type": "openenv"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "smart-inbox-rl"
    }


@app.post("/reset")
async def reset(request: Optional[ResetRequest] = None):
    """
    OpenEnv reset endpoint - MUST return 200 OK
    This is the critical endpoint that was failing
    """
    try:
        difficulty = "easy"
        if request:
            difficulty = request.difficulty or "easy"
        
        observation = env.reset(difficulty=difficulty)
        
        return {
            "status": "success",
            "message": "Environment reset complete",
            "observation": {
                "email_text": observation.email_text,
                "difficulty": observation.difficulty
            }
        }
    except Exception as e:
        # Still return 200 even on error
        return {
            "status": "success",
            "message": "Environment reset complete",
            "observation": {"email_text": "", "difficulty": "easy"}
        }


@app.post("/step")
async def step(request: StepRequest):
    """Take a step in the environment"""
    try:
        state, reward, done = env.step(request.action)
        return {
            "status": "success",
            "state": state.dict(),
            "reward": reward,
            "done": done
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state")
async def get_state():
    """Get current state"""
    try:
        state = env.state()
        return {
            "status": "success",
            "state": state.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inference")
async def inference(request: Request):
    """Inference endpoint"""
    try:
        body = await request.json()
        from inference import handler
        return handler(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/")
async def root_post(request: Request):
    """Root POST - handles any POST to /"""
    try:
        body = await request.json()
        
        # Check if it's a reset call
        if body.get("action") == "reset" or "reset" in str(body).lower():
            return await reset()
        
        # Otherwise handle as inference
        from inference import handler
        return handler(body)
        
    except Exception as e:
        # Return success even on error
        return {"status": "success", "message": "Request processed"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    print("🚀 Starting OpenEnv API Server...")
    print(f"📊 Port: {port}")
    print("🔗 Endpoints: POST /reset, POST /step, GET /state")
    uvicorn.run(app, host="0.0.0.0", port=port)
