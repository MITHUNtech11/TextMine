import os
import shutil
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Literal

from config.settings import API_TITLE, API_HOST, API_PORT, SUPPORTED_EXTENSIONS
from models.schemas import ResumeRoot
from orchestrator.orchestrator import (
    ResumeParsingOrchestrator, 
    OfflineParseResponse, 
    OnlineParseResponse
)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description="TextMine: Intelligent text extraction from images and documents using AI agents and OCR",
    version="2.0"
)

# Allow static frontends (for example GitHub Pages) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse_resume/offline", response_model=OfflineParseResponse)
async def parse_resume_offline(file: UploadFile = File(...)):
    """
    OCR-only parsing endpoint (no network required)
    
    Returns raw extracted text with confidence metrics.
    Perfect for offline deployment.
    """
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize orchestrator in offline mode
        orchestrator = ResumeParsingOrchestrator(mode="offline")
        result = orchestrator.process(temp_file_path, temp_dir)
        
        return result
    
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Configuration Error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        for temp_file in Path(temp_dir).glob(f"{Path(file.filename).stem}_temp*"):
            try:
                os.remove(temp_file)
            except:
                pass


@app.post("/parse_resume/online", response_model=OnlineParseResponse)
async def parse_resume_online(file: UploadFile = File(...)):
    """
    High-accuracy document text extraction and reconstruction using OCR + Gemini AI.
    
    Returns clean, error-corrected readable text along with structured sections and metadata.
    Requires internet connection and Google API key.
    """
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize orchestrator in online mode
        orchestrator = ResumeParsingOrchestrator(mode="online")
        result = orchestrator.process(temp_file_path, temp_dir)
        
        return result
    
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Configuration Error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        for temp_file in Path(temp_dir).glob(f"{Path(file.filename).stem}_temp*"):
            try:
                os.remove(temp_file)
            except:
                pass


@app.post("/parse_resume", response_model=OnlineParseResponse, deprecated=True)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    [DEPRECATED] Legacy endpoint - use /parse_resume/online instead
    
    Full parsing endpoint with OCR + Gemini
    """
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize orchestrator (defaults to online mode)
        orchestrator = ResumeParsingOrchestrator(mode="online")
        result = orchestrator.process(temp_file_path, temp_dir)
        
        return result
    
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Configuration Error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        for temp_file in Path(temp_dir).glob(f"{Path(file.filename).stem}_temp*"):
            try:
                os.remove(temp_file)
            except:
                pass


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0", "modes": ["offline", "online"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
