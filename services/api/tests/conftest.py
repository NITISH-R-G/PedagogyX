import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    client = TestClient(app)
    client.headers.update({"Authorization": "Bearer dev_api_key_placeholder"})
    return client
