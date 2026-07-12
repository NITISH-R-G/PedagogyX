import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.auth import verify_api_key

@pytest.fixture
def client():
    app.dependency_overrides[verify_api_key] = lambda: 'dev_api_key_placeholder'
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
