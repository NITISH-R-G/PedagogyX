import pytest


@pytest.fixture(autouse=True)
def auth_override(monkeypatch):
    monkeypatch.setenv("API_KEY", "dev_api_key_placeholder")
    from app.config import settings

    monkeypatch.setattr(settings, "api_key", "dev_api_key_placeholder")
