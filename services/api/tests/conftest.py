import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.auth import verify_api_key

app.dependency_overrides[verify_api_key] = lambda: 'dev_api_key_placeholder'

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
