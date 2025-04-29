"""Module for audio analysis endpoint."""

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    if not file.filename.endswith((".mp3", ".wav", ".m4a")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    analysis_result = {
        "filename": file.filename,
        "status": "analyzed",
        "tone": "neutral",
        "message": "Mock analysis complete",
    }

    return JSONResponse(content=analysis_result)
