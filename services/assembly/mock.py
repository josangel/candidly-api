"""Mock Assembly Service for testing purposes."""

from services.assembly.base import AssemblyBase


class MockAssemblyService(AssemblyBase):
    async def analyze_audio(self, audio_url: str) -> dict:
        return {
            "status": "analyzed",
            "tone": "neutral",
            "message": f"Mocked analysis for {audio_url}",
        }
