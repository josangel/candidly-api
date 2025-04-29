"""Conftest for the tests."""

import pytest


@pytest.fixture
def mock_upload_audio(mocker):
    return mocker.patch(
        "app.api.v1.endpoints.analyze.upload_audio",
        return_value="http://localhost/fake_audio.mp3",
    )


@pytest.fixture
def mock_analyze_audio(mocker):
    return mocker.patch(
        "app.api.v1.endpoints.analyze.ia_service.analyze_audio",
        return_value={"status": "analyzed", "filename": "test.mp3"},
    )
