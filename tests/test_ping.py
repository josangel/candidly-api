"""Module for testing the ping endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_ping_returns_pong():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        response = await client.get("http://test/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
