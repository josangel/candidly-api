from fastapi import APIRouter, File, UploadFile

from app.core.constants import ALLOWED_AUDIO_CONTENT_TYPES
from app.core.exceptions import (
    AnalyzeAudioException,
    InvalidAudioFormatException,
    UnexpectedAppException,
    UploadAudioException,
)
from app.deps.ai import ia_service
from app.services.s3 import upload_audio

router = APIRouter()


@router.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_AUDIO_CONTENT_TYPES:
        raise InvalidAudioFormatException()

    try:
        audio_url = upload_audio(file, file.filename)
        result = await ia_service.analyze_audio(audio_url)
        return result
    except (UploadAudioException, AnalyzeAudioException):
        raise
    except Exception as e:
        raise UnexpectedAppException(detail=str(e))
