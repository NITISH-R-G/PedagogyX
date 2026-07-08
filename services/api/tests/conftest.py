import pytest

from app.main import app
from app.auth import verify_api_key

@pytest.fixture
def client():
    # Only import TestClient inside the fixture or lazily to avoid triggering global effects if not needed?
    # Actually, importing TestClient is fine, but we need to ensure app.dependency_overrides is managed properly.
    from fastapi.testclient import TestClient
    app.dependency_overrides[verify_api_key] = lambda: "dev_api_key_placeholder"

    # We yield the TestClient without context manager to avoid triggering lifespan events globally in the fixture.
    # Note: TestClient(app) without 'with' statement still creates the client but won't trigger lifespan events in the same way,
    # OR we can just use the context manager.
    # The code reviewer mentioned: "Using TestClient as a context manager automatically triggers FastAPI's lifespan startup and shutdown events...
    # Because the automated refactoring script blindly injected the client fixture into almost every test... the lifespan events will now run before the test-level mocks are applied."
    # So we should yield a plain instance without context manager if tests don't explicitly require lifespan execution,
    # OR we just don't use 'with' in the fixture. Let's yield TestClient(app).
    yield TestClient(app)

    app.dependency_overrides.clear()
