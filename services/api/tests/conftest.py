import pytest
from app.config import settings


@pytest.fixture(autouse=True)
def mock_api_key(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "dev_api_key_placeholder")
