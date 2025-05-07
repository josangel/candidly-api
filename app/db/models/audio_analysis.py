"""Analysis model for audio files."""

import enum
from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, Enum, String, Text
from sqlalchemy.sql import func

from app.db.base import Base


class AnalysisStatus(str, enum.Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"


class AudioAnalysis(Base):
    __tablename__ = "audio_analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    filename = Column(String, nullable=False)
    audio_url = Column(String, nullable=False)
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.processing)

    transcript_text = Column(Text, nullable=True)
    assembly_response = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
