import pytest
from unittest.mock import patch
from app.main import app, lifespan
from fastapi.routing import APIRoute

@pytest.mark.asyncio
async def test_lifespan_success():
    with patch("app.main.minio_client.ensure_bucket") as mock_ensure_bucket:
        async with lifespan(None):
            pass
        mock_ensure_bucket.assert_called_once()

@pytest.mark.asyncio
async def test_lifespan_exception(capsys):
    with patch("app.main.minio_client.ensure_bucket", side_effect=Exception("Test Error")) as mock_ensure_bucket:
        async with lifespan(None):
            pass
        mock_ensure_bucket.assert_called_once()

    captured = capsys.readouterr()
    assert "WARN: MinIO bucket init skipped: Test Error" in captured.err

def test_app_configuration():
    assert app.title == "PedagogyX API"
    assert app.version == "0.2.1-dat"
    # lifespan context is wrapped by FastAPI, we can't assert identity directly.

def test_app_routers():
    # Verify some expected routes are present in the app to confirm routers are included correctly
    routes = [route.path for route in app.routes if isinstance(route, APIRoute)]

    assert "/health" in routes
    assert "/v1/sessions" in routes
    assert "/v1/dat-sessions" in routes # from dat_router
