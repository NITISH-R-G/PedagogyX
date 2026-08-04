import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import verify_api_key

def override_verify_api_key():
    return "dev_api_key_placeholder"

@pytest.fixture(autouse=True)
def auth_client():
    app.dependency_overrides[verify_api_key] = override_verify_api_key
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}
