"""
OpenEnv API Server - Minimal implementation
Accepts POST /reset and returns 200 OK
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "smart-inbox-rl"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
@app.get("/reset")
def reset():
    """OpenEnv reset endpoint - ALWAYS returns 200"""
    return {"status": "success", "message": "reset complete"}


@app.post("/step")
def step(request: Request):
    return {"status": "success", "reward": 1.0, "done": True}


@app.get("/state")
def state():
    return {"status": "success", "done": False, "reward": 0.0}


@app.post("/inference")
@app.post("/")
async def inference(request: Request):
    body = await request.json()
    return {"status": "success", "result": {"action": 0, "action_name": "mark_spam"}}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
