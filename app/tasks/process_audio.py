import logging

from celery import shared_task
from sqlalchemy import update

from app.db.models.audio_analysis import AudioAnalysis
from app.db.session import AsyncSessionLocal
from app.schemas.enums import AnalysisStatus
from app.services.assembly import ia_service

logger = logging.getLogger(__name__)


@shared_task(name="process_audio_task")
def process_audio_task(analysis_id: str, audio_url: str):
    """Celery task to process audio with AssemblyAI and store result in DB."""
    import asyncio

    async def run():
        async with AsyncSessionLocal() as session:
            try:
                result = await ia_service.analyze_audio(audio_url)
                logger.info("✅ Análisis completado para %s", analysis_id)

                stmt = (
                    update(AudioAnalysis)
                    .where(AudioAnalysis.id == analysis_id)
                    .values(
                        status=AnalysisStatus.analyzed,
                        transcript_text=result.get("transcript", ""),
                        summary=result.get("summary", ""),
                    )
                )
                await session.execute(stmt)
                await session.commit()
            except Exception as e:
                logger.error(
                    "❌ Falló el análisis con IA para %s: %s",
                    analysis_id,
                    str(e),
                )
                stmt = (
                    update(AudioAnalysis)
                    .where(AudioAnalysis.id == analysis_id)
                    .values(status=AnalysisStatus.failed)
                )
                await session.execute(stmt)
                await session.commit()

    asyncio.run(run())
