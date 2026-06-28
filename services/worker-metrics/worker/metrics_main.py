import json
import os
import sys
import traceback
from datetime import datetime, timezone

import psycopg2
import redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
DATABASE_URL = os.environ.get("DATABASE_URL", None)
JOB_QUEUE = os.environ.get("JOB_QUEUE", "jobs:talk_ratio")
JOB_QUEUE_DLQ = f"{JOB_QUEUE}:dlq"
POLL_TIMEOUT = int(os.environ.get("POLL_TIMEOUT", "5"))
PREVIEW_TEACHER_RATIO = float(os.environ.get("PREVIEW_TEACHER_RATIO", "0.68"))


def _compute_talk_ratio(cur, session_id: str) -> tuple[float, float, str]:
    cur.execute(
        "SELECT segments_json::text FROM session_transcripts WHERE session_id = %s",
        (session_id,),
    )
    row = cur.fetchone()
    if not row:
        teacher = PREVIEW_TEACHER_RATIO
        return teacher, round(1.0 - teacher, 4), "preview_stub"

    segments = json.loads(row[0]) if row[0] else []
    if not segments:
        teacher = PREVIEW_TEACHER_RATIO
        return teacher, round(1.0 - teacher, 4), "preview_stub"

    teacher_dur = 0.0
    total_dur = 0.0
    for i, seg in enumerate(segments):
        dur = max(0.0, float(seg.get("end", 0)) - float(seg.get("start", 0)))
        total_dur += dur
        if i % 2 == 0:
            teacher_dur += dur
    if total_dur <= 0:
        teacher = PREVIEW_TEACHER_RATIO
        return teacher, round(1.0 - teacher, 4), "preview_heuristic"

    teacher = round(teacher_dur / total_dur, 4)
    return teacher, round(1.0 - teacher, 4), "preview_heuristic"


def process_job(payload: dict) -> None:
    session_id = payload["session_id"]
    now = datetime.now(timezone.utc)

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            teacher, student, confidence = _compute_talk_ratio(cur, session_id)
            cur.execute(
                "SELECT completed_at FROM sessions WHERE id = %s",
                (session_id,),
            )
            completed = cur.fetchone()
            latency = None
            if completed and completed[0]:
                latency = (now - completed[0].replace(tzinfo=timezone.utc)).total_seconds()

            cur.execute(
                """
                INSERT INTO session_metrics (
                    session_id, teacher_talk_ratio, student_talk_ratio,
                    metric_confidence, preview_ready_at, insight_latency_sec, updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE
                SET teacher_talk_ratio = EXCLUDED.teacher_talk_ratio,
                    student_talk_ratio = EXCLUDED.student_talk_ratio,
                    metric_confidence = EXCLUDED.metric_confidence,
                    preview_ready_at = EXCLUDED.preview_ready_at,
                    insight_latency_sec = EXCLUDED.insight_latency_sec,
                    updated_at = EXCLUDED.updated_at
                """,
                (session_id, teacher, student, confidence, now, latency, now),
            )
        conn.commit()

    print(
        f"[worker-metrics] session={session_id} teacher={teacher:.0%} "
        f"latency_sec={latency} confidence={confidence}",
        flush=True,
    )


def main() -> None:
    client = redis.from_url(REDIS_URL, decode_responses=True)
    print(f"[worker-metrics] listening on {JOB_QUEUE}", flush=True)
    while True:
        item = client.blpop(JOB_QUEUE, timeout=POLL_TIMEOUT)
        if not item:
            continue
        _, raw = item
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            print(f"[worker-metrics] invalid job: {raw!r}", file=sys.stderr, flush=True)
            continue
        try:
            process_job(payload)
        except Exception as exc:
            print(f"[worker-metrics] job failed: {exc}", file=sys.stderr, flush=True)
            traceback.print_exc(file=sys.stderr)
            client.rpush(JOB_QUEUE_DLQ, raw)


if __name__ == "__main__":
    main()
