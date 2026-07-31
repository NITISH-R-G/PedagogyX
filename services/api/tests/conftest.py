import pytest
from app.main import app

@pytest.fixture(autouse=True)
def override_dependency():
    from app.auth import verify_api_key
    app.dependency_overrides[verify_api_key] = lambda: 'mock'
    yield
    app.dependency_overrides.clear()
