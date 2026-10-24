import pytest
from unittest.mock import patch
from app.main import lifespan


@pytest.mark.asyncio
async def test_lifespan_success():
    with patch("app.main.minio_client.ensure_bucket") as mock_ensure_bucket:
        async with lifespan(None):
            pass
        mock_ensure_bucket.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_exception(capsys):
    with patch(
        "app.main.minio_client.ensure_bucket", side_effect=Exception("Test Error")
    ) as mock_ensure_bucket:
        async with lifespan(None):
            pass
        mock_ensure_bucket.assert_called_once()

    captured = capsys.readouterr()
    assert "WARN: MinIO bucket init skipped: Test Error" in captured.err
