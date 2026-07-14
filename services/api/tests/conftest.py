import pytest
from fastapi.testclient import TestClient

from app.auth import verify_api_key
from app.main import app

@pytest.fixture
def client():
    app.dependency_overrides[verify_api_key] = lambda: 'dev_api_key_placeholder'
    yield TestClient(app)
    app.dependency_overrides.clear()
