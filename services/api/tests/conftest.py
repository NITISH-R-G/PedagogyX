import pytest
from app.main import app
from app.auth import verify_api_key

@pytest.fixture(autouse=True)
def bypass_auth():
    app.dependency_overrides[verify_api_key] = lambda: 'mock_api_key'
    yield
    app.dependency_overrides = {}
