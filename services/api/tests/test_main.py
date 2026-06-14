import pytest
from unittest.mock import patch
from app.main import lifespan

@pytest.mark.asyncio
@patch("app.main.db_utils.init_pool")
@patch("app.main.db_utils.close_pool")
async def test_lifespan_success(mock_close_pool, mock_init_pool):
    with patch("app.main.minio_client.ensure_bucket") as mock_ensure_bucket:
        async with lifespan(None):
            mock_init_pool.assert_called_once()
        mock_ensure_bucket.assert_called_once()
        mock_close_pool.assert_called_once()

@pytest.mark.asyncio
@patch("app.main.db_utils.init_pool")
@patch("app.main.db_utils.close_pool")
async def test_lifespan_exception(mock_close_pool, mock_init_pool, capsys):
    with patch("app.main.minio_client.ensure_bucket", side_effect=Exception("Test Error")) as mock_ensure_bucket:
        async with lifespan(None):
            mock_init_pool.assert_called_once()
        mock_ensure_bucket.assert_called_once()
        mock_close_pool.assert_called_once()

    captured = capsys.readouterr()
    assert "WARN: MinIO bucket init skipped: Test Error" in captured.err
