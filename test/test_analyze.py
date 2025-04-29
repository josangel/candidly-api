"""Module for testing the audio analysis endpoint."""

from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_analyze_audio_with_valid_file():
    """Test the audio analysis endpoint with a valid audio file."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        audio_data = BytesIO(b"fake audio data")
        files = {"file": ("test.mp3", audio_data, "audio/mpeg")}
        response = await client.post("http://test/api/v1/analyze", files=files)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "analyzed"
    assert json_data["filename"] == "test.mp3"


@pytest.mark.asyncio
async def test_analyze_audio_with_invalid_file():
    """Test the audio analysis endpoint with an invalid audio file."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        audio_data = BytesIO(b"not an audio file")
        files = {"file": ("test.txt", audio_data, "text/plain")}
        response = await client.post("http://test/api/v1/analyze", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"
