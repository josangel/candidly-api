"""Module for AssemblyAI service in production environment."""

import httpx

from services.assembly.base import AssemblyBase


class AssemblyService(AssemblyBase):
    async def analyze_audio(self, audio_url: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url="https://api.assemblyai.com/v2/analyze",
                json={"audio_url": audio_url},
            )
            return resp.json()
