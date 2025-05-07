from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class AudioAnalysisOut(BaseModel):
    id: UUID4
    filename: str
    status: str
    audio_url: Optional[str]
    transcript_text: Optional[str]
    summary: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
