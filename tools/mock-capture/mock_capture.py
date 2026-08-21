import asyncio
import os
from pathlib import Path

import httpx

API_URL = os.environ.get("API_URL", "http://localhost:8000")
API_KEY = os.environ.get("API_KEY", "dev_api_key_placeholder")

# Sample data
SAMPLE_AUDIO = Path(__file__).parent.parent.parent / "benchmarks/results/_sample_silence.wav"


async def main():
    if not SAMPLE_AUDIO.exists():
        # create a dummy wav file if it doesn't exist
        SAMPLE_AUDIO.parent.mkdir(parents=True, exist_ok=True)
        SAMPLE_AUDIO.write_bytes(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00")

    print(f"Mocking capture agent. API_URL={API_URL}")
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {API_KEY}"}) as client:
        print("1. Starting session...")
        res = await client.post(f"{API_URL}/v1/capture/start", json={"school_id": "school_1"})
        res.raise_for_status()
        session_id = res.json()["session_id"]
        print(f"Session started: {session_id}")

        print("2. Uploading chunk...")
        await upload_chunk(client, API_URL, session_id, 0, SAMPLE_AUDIO)

        print("3. Completing session...")
        res = await client.post(f"{API_URL}/v1/capture/{session_id}/complete")
        res.raise_for_status()
        print("Session completed.")


async def upload_chunk(
    client: httpx.AsyncClient, base: str, session_id: str, chunk_index: int, audio_path: Path
) -> None:
    file_content = audio_path.read_bytes()
    res = await client.post(
        f"{base}/v1/capture/{session_id}/chunk",
        data={"chunk_index": chunk_index},
        files={"file": ("chunk.wav", file_content, "audio/wav")},
    )
    res.raise_for_status()


if __name__ == "__main__":
    asyncio.run(main())
