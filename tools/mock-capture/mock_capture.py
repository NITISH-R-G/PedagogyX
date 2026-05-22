#!/usr/bin/env python3
"""Stub capture agent: create + complete a session (no real media upload yet)."""

from __future__ import annotations

import argparse
import sys

import httpx

DEFAULT_API = "http://localhost:8080"


def main() -> int:
    parser = argparse.ArgumentParser(description="PedagogyX mock capture (boilerplate)")
    parser.add_argument("--api-url", default=DEFAULT_API)
    parser.add_argument("--school-id", default="pilot-school-dev")
    parser.add_argument("--room-id", default="room-1")
    parser.add_argument("--teacher-id", default="teacher-dev")
    args = parser.parse_args()

    base = args.api_url.rstrip("/")
    with httpx.Client(timeout=30.0) as client:
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
        print(f"Upload hint: {body.get('upload_hint')}")

        done = client.post(f"{base}/v1/sessions/{session_id}/complete")
        done.raise_for_status()
        print(f"Session completed: {done.json()}")

    print("Mock capture OK — check worker-asr logs for STUB job")
    return 0


if __name__ == "__main__":
    sys.exit(main())
