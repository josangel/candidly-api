"""Mock Assembly Service for testing purposes."""

from .base import AssemblyBase


class MockAssemblyService(AssemblyBase):
    async def analyze_audio(self, audio_url: str) -> dict:
        return {
            "transcript": "Esto es un mock de transcripción.",
            "summary": "Resumen generado localmente.",
            "tone": "neutral",
        }
