"""Module to handle audio analysis using AssemblyAI API."""

import os

import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

transcriber = aai.Transcriber()


async def analyze_audio_from_url(audio_url: str) -> dict:
    try:
        transcript = await transcriber.transcribe_async(audio_url)

        return transcript
    except Exception as e:
        return {"status": "error", "detail": str(e)}
