"""Module for AssemblyBase class."""

from abc import ABC, abstractmethod


class AssemblyBase(ABC):
    @abstractmethod
    async def analyze_audio(self, audio_url: str) -> dict:
        """Analyze audio and return transcript/summary."""
        pass
