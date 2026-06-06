import time
import redis
import json
import os
from datetime import datetime, timezone

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
JOB_QUEUE_METRICS = "jobs:talk_ratio_test"

def _enqueue_metrics_original(session_id: str, school_id: str) -> None:
    client = redis.from_url(REDIS_URL, decode_responses=True)
    payload = {
        "job_type": "talk_ratio",
        "session_id": session_id,
        "school_id": school_id,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
    }
    client.rpush(JOB_QUEUE_METRICS, json.dumps(payload))

_redis_client = None

def _get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client

def _enqueue_metrics_optimized(session_id: str, school_id: str) -> None:
    client = _get_redis_client()
    payload = {
        "job_type": "talk_ratio",
        "session_id": session_id,
        "school_id": school_id,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
    }
    client.rpush(JOB_QUEUE_METRICS, json.dumps(payload))

def run_benchmark(iterations=1000):
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
    except Exception as e:
        print(f"Redis not available: {e}")
        return

    r.delete(JOB_QUEUE_METRICS)

    start_time = time.perf_counter()
    for i in range(iterations):
        _enqueue_metrics_original(f"sess_{i}", f"school_{i}")
    orig_time = time.perf_counter() - start_time

    r.delete(JOB_QUEUE_METRICS)

    start_time = time.perf_counter()
    for i in range(iterations):
        _enqueue_metrics_optimized(f"sess_{i}", f"school_{i}")
    opt_time = time.perf_counter() - start_time

    print(f"Original time: {orig_time:.4f}s")
    print(f"Optimized time: {opt_time:.4f}s")
    print(f"Improvement: {orig_time / opt_time:.2f}x")

if __name__ == '__main__':
    run_benchmark()
