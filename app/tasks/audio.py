import boto3
from sqlalchemy import update

from app.db.models.audio_analysis import AudioAnalysis
from app.db.session import AsyncSessionLocal
from app.worker import celery_app


@celery_app.task
def upload_audio_to_s3_task(analysis_id: str, file_path: str):
    from core.config import settings

    s3 = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    # Upload the file to S3
    s3_key = f"{analysis_id}.mp3"
    s3.upload_file(file_path, settings.s3_bucket, s3_key)

    audio_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"

    # Update database with the audio URL
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
