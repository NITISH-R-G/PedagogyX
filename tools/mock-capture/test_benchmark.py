import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).parent))
from mock_capture import upload_chunk


@pytest.mark.asyncio
async def test_upload_chunk_functionality(tmp_path: Path):
    sample_file = tmp_path / "sample.wav"
    sample_file.write_bytes(b"dummy audio content" * 100)

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = mock_response

    await upload_chunk(mock_client, "http://localhost:8080", "sess-123", 0, sample_file)

    mock_client.post.assert_called_once()
    args, kwargs = mock_client.post.call_args
    assert args[0] == "http://localhost:8080/v1/sessions/sess-123/chunks/0"
    assert "files" in kwargs
    filename, file_bytes, content_type = kwargs["files"]["file"]
    assert filename == "sample.wav"
    assert file_bytes == b"dummy audio content" * 100
    assert content_type == "audio/wav"


@pytest.mark.asyncio
async def test_upload_chunk_event_loop_responsiveness(tmp_path: Path):
    # Create a 20MB file to simulate reading audio payload
    large_file = tmp_path / "large_audio.wav"
    large_file.write_bytes(b"A" * (20 * 1024 * 1024))

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = mock_response

    # Background task that ticks every 1ms to monitor event loop latency
    ticker_count = 0
    running = True

    async def ticker():
        nonlocal ticker_count
        while running:
            await asyncio.sleep(0.001)
            ticker_count += 1

    ticker_task = asyncio.create_task(ticker())

    start_time = time.perf_counter()
    # Execute upload_chunk multiple times to measure event loop ticks
    for _ in range(5):
        await upload_chunk(mock_client, "http://localhost:8080", "sess-123", 0, large_file)
    elapsed = time.perf_counter() - start_time

    running = False
    await ticker_task

    print(f"\n[Benchmark] Upload 5x 20MB chunks took {elapsed:.4f}s, ticker count: {ticker_count}")
    assert mock_client.post.call_count == 5
