import pytest
from app.main import app
from app.auth import verify_api_key
from fastapi.testclient import TestClient

@pytest.fixture(autouse=True)
def override_api_key():
    app.dependency_overrides[verify_api_key] = lambda: 'mock_api_key'
    yield
    app.dependency_overrides = {}
