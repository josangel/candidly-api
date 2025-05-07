import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="upload_audio_to_s3_task")
def upload_audio_to_s3_task(analysis_id: str, file_path: str):
    try:
        import asyncio
        import os

        import boto3
        from sqlalchemy import update

        from app.core.config import settings
        from app.db.models.audio_analysis import AudioAnalysis
        from app.db.session import AsyncSessionLocal

        s3 = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

        s3_key = f"{analysis_id}.mp3"
        s3.upload_file(file_path, settings.s3_bucket, s3_key)
        audio_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"

        async def update_db():
            async with AsyncSessionLocal() as session:
                stmt = (
                    update(AudioAnalysis)
                    .where(AudioAnalysis.id == analysis_id)
                    .values(audio_url=audio_url)
                )
                await session.execute(stmt)
                await session.commit()
                logger.info(
                    "✅ Audio subido a S3 y DB actualizada para %s", analysis_id
                )

        asyncio.run(update_db())

    except Exception as e:
        logger.info(f"❌ Error al subir el audio o actualizar DB: {e}")
    finally:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
