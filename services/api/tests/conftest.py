import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="function", autouse=True)
def _mock_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "dev_api_key_placeholder")

@pytest.fixture(scope="function")
def client():
    # Make sure we don't accidentally reuse the same client across tests
    # without resetting headers if something modifies them
    test_client = TestClient(app)
    test_client.headers.update({"Authorization": "Bearer dev_api_key_placeholder"})
    return test_client
