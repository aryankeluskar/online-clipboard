import os
import hashlib
import time
from typing import Dict, Union, Optional
from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.responses import JSONResponse
import redis
import json

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Fast Clipboard API")

# Redis connection with Redis Cloud credentials
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True,
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
)

# Maximum content size (10MB in bytes)
MAX_CONTENT_SIZE = 10 * 1024 * 1024  # 10MB

# Expiration time in seconds (24 hours)
EXPIRY_TIME = 24 * 60 * 60  # 24 hours


@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Fast Clipboard API", 
        "info": "Use POST / to create a clipboard and GET /{id} to retrieve it"
    }


@app.get("/{clipboard_id}")
async def get_content(clipboard_id: str):
    """
    Retrieve content from the clipboard by ID
    """
    try:
        # Check if the clipboard exists in Redis
        content = redis_client.get(f"clipboard:{clipboard_id}")
        
        if not content:
            raise HTTPException(status_code=404, detail="Clipboard not found or has expired")
        
        return {"content": content}
    except redis.RedisError as e:
        print(f"Redis error retrieving content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {str(e)}")
    except Exception as e:
        print(f"Error retrieving content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {str(e)}")


@app.post("/")
async def update_content(request: Request):
    """
    Create a new clipboard and return a hash ID with 24-hour expiry
    """
    try:
        # Get raw content from request
        content = await request.body()
        
        # Convert bytes to string if needed
        if isinstance(content, bytes):
            try:
                content = content.decode('utf-8')
            except UnicodeDecodeError:
                # If it's binary data, keep as is
                pass
        
        # Check content size
        content_size = len(content.encode('utf-8') if isinstance(content, str) else content)
        if content_size > MAX_CONTENT_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"Content too large. Maximum size is {MAX_CONTENT_SIZE/1024/1024}MB"
            )
        
        # Generate a hash ID based on content and timestamp
        timestamp = str(time.time())
        hash_input = f"{content}{timestamp}".encode('utf-8') if isinstance(content, str) else content + timestamp.encode('utf-8')
        clipboard_id = hashlib.sha256(hash_input).hexdigest()[:16]
        
        # Store content in Redis with expiration
        redis_client.setex(f"clipboard:{clipboard_id}", EXPIRY_TIME, content)
        
        return {
            "message": "Content updated successfully",
            "clipboard_id": clipboard_id,
            "expires_in": f"{EXPIRY_TIME/60/60} hours"
        }
    except redis.RedisError as e:
        print(f"Redis error updating content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating content: {str(e)}")
    except Exception as e:
        print(f"Error updating content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating content: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """
    Ensure Redis connection is working on startup
    """
    try:
        redis_client.ping()
        print("Successfully connected to Redis")
    except redis.RedisError as e:
        print(f"Redis connection error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 