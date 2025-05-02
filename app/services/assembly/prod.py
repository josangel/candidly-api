"""Module for AssemblyAI service in production environment."""

import assemblyai as aai

from app.core.config import settings

from .base import AssemblyBase


class RealAssemblyService(AssemblyBase):

    async def analyze_audio(self, audio_url: str) -> dict:
        aai.settings.api_key = settings.assemblyai_api_key
        transcriber = aai.Transcriber(
            config=aai.TranscriptionConfig(sentiment_analysis=True)
        )
        transcript = transcriber.transcribe(audio_url)
        acoustic_analysis = transcript.get("acoustic_analysis", {})
        return {
            "transcript": transcript.text,
            "summary": transcript.get("summary", ""),
            "tone": acoustic_analysis.get("overall", "unknown"),
        }
