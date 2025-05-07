import shutil
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audio_analysis import AnalysisStatus, AudioAnalysis
from app.db.session import AsyncSessionLocal, get_db
from app.schemas.audio_analysis import AudioAnalysisOut
from app.tasks.process_audio import process_audio_task
from app.tasks.upload_audio import upload_audio_to_s3_task

router = APIRouter()


@router.post("/analyze", status_code=201)
async def analyze_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type",
        )

    temp_dir = "/tmp/audio"
    file_path = f"{temp_dir}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    analysis_id = str(uuid4())
    async with AsyncSessionLocal() as session:
        audio = AudioAnalysis(
            id=analysis_id,
            filename=file.filename,
            audio_url="pending",
            status=AnalysisStatus.processing,
        )
        session.add(audio)
        await session.commit()

    upload_audio_to_s3_task.delay(analysis_id, file_path)
    process_audio_task.delay(analysis_id, file_path)

    return {"id": analysis_id, "status": "processing"}


@router.get("/analyze/{analysis_id}", response_model=AudioAnalysisOut)
async def get_audio_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    analysis = await db.get(AudioAnalysis, str(analysis_id))
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
