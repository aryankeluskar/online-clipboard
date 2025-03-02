import os
from typing import Dict, Union
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
import shutil

app = FastAPI(title="Fast Clipboard API")

# Use /tmp directory which is writable in most serverless environments
CONTENT_DIR = "/tmp/content"
os.makedirs(CONTENT_DIR, exist_ok=True)

# Default content file path
CONTENT_FILE = os.path.join(CONTENT_DIR, "clipboard.txt")


@app.get("/")
async def get_content():
    """
    Retrieve all content from the clipboard
    """
    try:
        # Check if the content file exists
        if not os.path.exists(CONTENT_FILE):
            # Return empty content if file doesn't exist
            return {"content": ""}
        
        # Read content from the file
        with open(CONTENT_FILE, "r") as f:
            content = f.read()
        
        return {"content": content}
    except Exception as e:
        print(f"Error retrieving content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {str(e)}")


@app.post("/")
async def update_content(content: str = Body(..., embed=True)):
    """
    Update all content in the clipboard
    """
    try:
        # Ensure the content directory exists
        os.makedirs(CONTENT_DIR, exist_ok=True)
        
        # Write content to the file
        with open(CONTENT_FILE, "w") as f:
            f.write(content)
        
        return {"message": "Content updated successfully"}
    except Exception as e:
        print(f"Error updating content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating content: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 