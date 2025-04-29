"""Tests for the /analyze endpoint covering success and all error paths."""

from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.exceptions import AnalyzeAudioException, UploadAudioException
from app.main import app


@pytest.mark.asyncio
async def test_analyze_success(mock_upload_audio, mock_analyze_audio):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        files = {
            "file": ("test.mp3", BytesIO(b"valid audio data"), "audio/mpeg"),
        }
        response = await client.post("http://test/api/v1/analyze", files=files)

    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data


@pytest.mark.asyncio
async def test_analyze_invalid_file_type():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        files = {
            "file": ("not_audio.txt", BytesIO(b"not audio"), "text/plain"),
        }
        response = await client.post("http://test/api/v1/analyze", files=files)

    resp_detail = response.json()["detail"]
    assert response.status_code == 400
    assert resp_detail == "Invalid file type. Accepted formats: .mp3, .wav"


@pytest.mark.asyncio
async def test_analyze_upload_error(mocker, mock_analyze_audio):
    mocker.patch(
        "app.api.v1.endpoints.analyze.upload_audio",
        side_effect=UploadAudioException("Upload failed"),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        files = {"file": ("test.mp3", BytesIO(b"audio"), "audio/mpeg")}
        response = await client.post("http://test/api/v1/analyze", files=files)

    assert response.status_code == 500
    assert response.json()["detail"] == "Upload failed"


@pytest.mark.asyncio
async def test_analyze_ia_error(mocker, mock_upload_audio):
    mocker.patch(
        "app.api.v1.endpoints.analyze.ia_service.analyze_audio",
        side_effect=AnalyzeAudioException("Assembly service down"),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        files = {"file": ("test.mp3", BytesIO(b"audio"), "audio/mpeg")}
        response = await client.post("http://test/api/v1/analyze", files=files)

    assert response.status_code == 502
    assert response.json()["detail"] == "Assembly service down"


@pytest.mark.asyncio
async def test_analyze_unexpected_error(mocker, mock_upload_audio):
    mocker.patch(
        "app.api.v1.endpoints.analyze.ia_service.analyze_audio",
        side_effect=Exception("Kaboom!"),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        files = {"file": ("test.mp3", BytesIO(b"audio"), "audio/mpeg")}
        response = await client.post("http://test/api/v1/analyze", files=files)

    assert response.status_code == 500
    assert "Kaboom!" in response.json()["detail"]
