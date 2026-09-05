import json
from datetime import datetime, timezone
from uuid import UUID

import redis

from app.config import settings


def get_redis() -> redis.Redis:
    return redis.from_url(settings.redis_url, decode_responses=True)


def enqueue_asr_job(session_id: UUID, school_id: str) -> None:
    payload = {
        "job_type": "asr",
        "session_id": str(session_id),
        "school_id": school_id,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
    }
    get_redis().rpush(settings.job_queue_asr, json.dumps(payload))


def enqueue_talk_ratio_job(session_id: UUID, school_id: str) -> None:
    payload = {
        "job_type": "talk_ratio",
        "session_id": str(session_id),
        "school_id": school_id,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
    }
    get_redis().rpush(settings.job_queue_metrics, json.dumps(payload))
