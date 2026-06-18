import json
import os
import sys
import traceback

import redis

from worker.processor import process_job

REDIS_URL = os.environ.get("REDIS_URL", None)
JOB_QUEUE = os.environ.get("JOB_QUEUE", "jobs:asr")
JOB_QUEUE_DLQ = f"{JOB_QUEUE}:dlq"
POLL_TIMEOUT = int(os.environ.get("POLL_TIMEOUT", "5"))


def main() -> None:
    client = redis.from_url(REDIS_URL, decode_responses=True) # type: ignore
    mode = os.environ.get("WORKER_MODE", "stub")
    print(f"[worker-asr] listening on {JOB_QUEUE} (mode={mode})", flush=True)
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
            traceback.print_exc(file=sys.stderr)
            client.rpush(JOB_QUEUE_DLQ, raw)


if __name__ == "__main__":
    main()
