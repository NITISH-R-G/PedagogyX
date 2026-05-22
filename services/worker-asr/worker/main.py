import json
import os
import sys

import redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
JOB_QUEUE = os.environ.get("JOB_QUEUE", "jobs:asr")
WORKER_MODE = os.environ.get("WORKER_MODE", "stub")
POLL_TIMEOUT = int(os.environ.get("POLL_TIMEOUT", "5"))


def process_job(payload: dict) -> None:
    session_id = payload.get("session_id")
    print(f"[worker-asr] STUB processed session={session_id} mode={WORKER_MODE}", flush=True)
    # Sprint 03 S03-05: wire faster-whisper here


def main() -> None:
    client = redis.from_url(REDIS_URL, decode_responses=True)
    print(f"[worker-asr] listening on {JOB_QUEUE} ({WORKER_MODE})", flush=True)
    while True:
        item = client.blpop(JOB_QUEUE, timeout=POLL_TIMEOUT)
        if not item:
            continue
        _, raw = item
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            print(f"[worker-asr] invalid job: {raw!r}", file=sys.stderr, flush=True)
            continue
        try:
            process_job(payload)
        except Exception as exc:
            print(f"[worker-asr] job failed: {exc}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
