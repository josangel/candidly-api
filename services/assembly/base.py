"""Module for AssemblyAI base class."""


class AssemblyBase:
    async def analyze_audio(self, audio_url: str) -> dict:
        raise NotImplementedError
