# tasks/process_audio.py
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="process_audio_task")
def process_audio_task(analysis_id: str, file_path: str):
    import asyncio
    import os

    from sqlalchemy import update

    from app.db.models.audio_analysis import AudioAnalysis
    from app.db.session import AsyncSessionLocal
    from app.schemas.enums import AnalysisStatus
    from app.services.assembly import ia_service

    async def run():
        async with AsyncSessionLocal() as session:
            try:
                result = await ia_service.analyze_audio(file_path)
                logger.info("✅ Análisis completado para %s", analysis_id)

                stmt = (
                    update(AudioAnalysis)
                    .where(AudioAnalysis.id == analysis_id)
                    .values(
                        status=AnalysisStatus.completed,
                        transcript_text=result["transcript"],
                        assembly_response=result,
                    )
                )
                await session.execute(stmt)
                await session.commit()
            except Exception as e:
                logger.error(f"Error processing audio: {e}")
                stmt = (
                    update(AudioAnalysis)
                    .where(AudioAnalysis.id == analysis_id)
                    .values(status=AnalysisStatus.failed)
                )
                await session.execute(stmt)
                await session.commit()
            finally:
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    pass

    asyncio.run(run())
