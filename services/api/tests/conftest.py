import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    # Instantiate the client properly
    test_client = TestClient(app)
    test_client.headers.update({"Authorization": "Bearer dev_api_key_placeholder"})
    yield test_client
