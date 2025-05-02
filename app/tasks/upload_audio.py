# app/tasks/upload_audio.py
import boto3
from celery import shared_task
from sqlalchemy import update

from app.core.config import settings
from app.db.models.audio_analysis import AudioAnalysis
from app.db.session import AsyncSessionLocal
from app.tasks.process_audio import process_audio_task


@shared_task
def upload_audio_to_s3_task(analysis_id: str, file_path: str):
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

        s3_key = f"{analysis_id}.mp3"
        s3.upload_file(file_path, settings.s3_bucket, s3_key)

        audio_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"

        # Update DB with audio_url
        async def update_db():
            async with AsyncSessionLocal() as session:
                stmt = (
                    update(AudioAnalysis)
                    .where(AudioAnalysis.id == analysis_id)
                    .values(audio_url=audio_url)
                )
                await session.execute(stmt)
                await session.commit()

        import asyncio

        asyncio.run(update_db())

        # Trigger processing
        process_audio_task.delay(analysis_id, audio_url)

    except Exception as e:
        print(f"❌ Error al subir el audio o actualizar DB: {e}")
