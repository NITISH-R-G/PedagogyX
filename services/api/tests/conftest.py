import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import verify_api_key
import os

@pytest.fixture(autouse=True)
def override_api_key():
    os.environ["API_KEY"] = "dev_api_key_placeholder"
    app.dependency_overrides[verify_api_key] = lambda: "dev_api_key_placeholder"
    yield
    app.dependency_overrides.clear()
