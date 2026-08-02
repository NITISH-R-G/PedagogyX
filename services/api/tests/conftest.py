import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.auth import verify_api_key

@pytest.fixture(autouse=True)
def mock_auth():
    app.dependency_overrides[verify_api_key] = lambda: 'mock_api_key'
    yield
    app.dependency_overrides = {}

@pytest.fixture
def client():
    yield TestClient(app)
