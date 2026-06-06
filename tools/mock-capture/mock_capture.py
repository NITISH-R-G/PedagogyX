#!/usr/bin/env python3
"""Mock capture: create session, upload chunk, complete — triggers ASR + talk ratio pipeline."""

import argparse
import struct
import sys
import wave
from pathlib import Path

import httpx

DEFAULT_API = "http://localhost:8080"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def ensure_sample_wav(path: Path) -> Path:
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    sample_rate = 16000
    duration_sec = 3
    n_frames = sample_rate * duration_sec
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for _ in range(n_frames):
            wf.writeframes(struct.pack("<h", 0))
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="PedagogyX mock capture")
    parser.add_argument("--api-url", default=DEFAULT_API)
    parser.add_argument("--school-id", default="pilot-school-dev")
    parser.add_argument("--room-id", default="room-1")
    parser.add_argument("--teacher-id", default="teacher-dev")
    parser.add_argument("--chunk-index", type=int, default=0)
    parser.add_argument("--audio", type=Path, default=None, help="WAV/MP3 file to upload")
    args = parser.parse_args()

    base = args.api_url.rstrip("/")
    audio_path = args.audio
    if audio_path is None:
        audio_path = ensure_sample_wav(FIXTURE_DIR / "sample_3s.wav")

    with httpx.Client(timeout=120.0) as client:
        health = client.get(f"{base}/health")
        health.raise_for_status()
        print(f"API health: {health.json()}")

        created = client.post(
            f"{base}/v1/sessions",
            json={
                "school_id": args.school_id,
                "room_id": args.room_id,
                "teacher_id": args.teacher_id,
            },
        )
        created.raise_for_status()
        body = created.json()
        session_id = body["session_id"]
        print(f"Session created: {session_id}")

        with open(audio_path, "rb") as f:
            upload = client.post(
                f"{base}/v1/sessions/{session_id}/chunks/{args.chunk_index}",
                files={"file": (audio_path.name, f, "audio/wav")},
            )
        upload.raise_for_status()
        print(f"Chunk uploaded: {upload.json()}")

        done = client.post(f"{base}/v1/sessions/{session_id}/complete")
        done.raise_for_status()
        print(f"Session completed: {done.json()}")

        import time

        for _ in range(30):
            preview = client.get(f"{base}/v1/sessions/{session_id}/preview")
            preview.raise_for_status()
            data = preview.json()
            if data.get("preview_ready"):
                print(f"Preview ready: {data}")
                break
            time.sleep(1)
        else:
            print("WARN: preview not ready after 30s — check worker logs")

        overview = client.get(f"{base}/v1/schools/{args.school_id}/overview")
        overview.raise_for_status()
        m_a = overview.json().get("m_a_coverage", {})
        print(f"School overview M-A: {m_a}")

    print("Mock capture OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
