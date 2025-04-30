import shutil
import tempfile
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audio_analysis import AnalysisStatus, AudioAnalysis
from app.db.session import AsyncSessionLocal
from app.tasks.audio import upload_audio_to_s3_task

router = APIRouter()


@router.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type",
        )

    # Guardar archivo en tmp local para pasarlo a la tarea
    temp_dir = tempfile.mkdtemp()
    file_path = f"{temp_dir}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Crear registro en la base de datos
    session: AsyncSession = AsyncSessionLocal()
    analysis_id = str(uuid4())
    audio = AudioAnalysis(
        id=analysis_id,
        filename=file.filename,
        audio_url="pending",
        status=AnalysisStatus.processing,
    )
    session.add(audio)
    await session.commit()

    # Encolar tarea
    upload_audio_to_s3_task.delay(analysis_id, file_path)

    return {"id": analysis_id, "status": "processing"}
