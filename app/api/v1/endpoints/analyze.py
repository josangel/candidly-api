"""Module for audio analysis endpoint."""

from fastapi import APIRouter, File, UploadFile

from app.main import ia_service
from services.s3 import upload_audio

router = APIRouter()


@router.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    filename = file.filename
    audio_url = upload_audio(file, filename)
    result = await ia_service.analyze_audio(audio_url)
    return result
