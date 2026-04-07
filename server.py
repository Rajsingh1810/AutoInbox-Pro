"""
OpenEnv API Server for Smart Inbox Assistant
Combines Gradio web app with OpenEnv-required API endpoints
"""

import os
import json
import threading
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import gradio as gr

# Import the Gradio app
from app import demo as gradio_app

# Import inference engine
from inference import SmartInboxInference

app = FastAPI(title="Smart Inbox Assistant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global inference engine
inference_engine = SmartInboxInference()


class InferenceRequest(BaseModel):
    """Request model for inference"""
    inputs: dict
    
    class Config:
        extra = "allow"


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Smart Inbox Assistant",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": inference_engine.model_loaded,
        "service": "smart-inbox-assistant"
    }


@app.post("/reset")
async def reset():
    """
    Reset endpoint for OpenEnv validation
    This is the critical endpoint that OpenEnv calls
    """
    try:
        # Reset the inference engine
        global inference_engine
        inference_engine = SmartInboxInference()
        
        return {
            "status": "success",
            "message": "Inference engine reset complete"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inference")
async def inference(request: InferenceRequest):
    """Main inference endpoint"""
    try:
        inputs = request.inputs
        
        # Extract email text and difficulty
        if isinstance(inputs, str):
            email_text = inputs
            difficulty = "easy"
        elif isinstance(inputs, dict):
            email_text = inputs.get("text", inputs.get("email", ""))
            difficulty = inputs.get("difficulty", "easy")
        else:
            raise HTTPException(status_code=400, detail="Invalid input format")
        
        # Make prediction
        result = inference_engine.predict(email_text, difficulty)
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/")
async def root_post(request: Request):
    """
    Root POST endpoint - handles various request types
    OpenEnv may call POST / directly
    """
    try:
        body = await request.json()
        
        # Check if it's a reset call
        if body.get("action") == "reset" or "reset" in str(body).lower():
            global inference_engine
            inference_engine = SmartInboxInference()
            return {"status": "success", "message": "Reset complete"}
        
        # Otherwise treat as inference request
        return await inference(InferenceRequest(inputs=body))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_gradio():
    """Start Gradio app in a separate thread"""
    gradio_app.launch(
        server_name="0.0.0.0",
        server_port=7861,  # Different port for Gradio
        share=False,
        quiet=True
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    
    # Start Gradio in background thread
    gradio_thread = threading.Thread(target=start_gradio, daemon=True)
    gradio_thread.start()
    
    print("🚀 Starting Smart Inbox Assistant API Server...")
    print(f"📊 API on port {port}")
    print("🎨 Gradio UI on port 7861")
    
    # Run FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=port)
