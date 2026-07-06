import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import verify_api_key

@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[verify_api_key] = lambda: 'dev_api_key_placeholder'
    yield
    app.dependency_overrides = {}

@pytest.fixture
def client():
    return TestClient(app)
