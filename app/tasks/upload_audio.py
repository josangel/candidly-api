import logging
import os

import boto3
from celery import shared_task
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.audio_analysis import AudioAnalysis
from app.db.session import sync_engine

logger = logging.getLogger(__name__)


@shared_task
def upload_audio_to_s3_task(analysis_id: str, file_path: str):
    try:
        logger.info(f"🔄 Iniciando subida de {file_path} con ID {analysis_id}")

        s3 = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

        s3_key = f"{analysis_id}.mp3"
        s3.upload_file(file_path, settings.s3_bucket, s3_key)
        audio_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"

        logger.info(f"✅ Archivo subido a {audio_url}")

        with Session(sync_engine) as session:
            stmt = (
                update(AudioAnalysis)
                .where(AudioAnalysis.id == analysis_id)
                .values(audio_url=audio_url)
            )
            session.execute(stmt)
            session.commit()

        logger.info(
            f"✅ URL registrada en la base de datos para ID {analysis_id}",
        )

    except Exception as e:
        logger.error(f"❌ Error al subir el audio o actualizar DB: {e}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"🧹 Archivo temporal eliminado: {file_path}")
