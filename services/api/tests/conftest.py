import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(autouse=True)
def client():
    c = TestClient(app)
    c.headers.update({"Authorization": "Bearer dev_api_key_placeholder"})
    return c
