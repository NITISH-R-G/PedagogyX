import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone

import boto3
import psycopg2
import redis
from botocore.client import Config
from botocore.exceptions import ClientError
from psycopg2.extras import Json

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://pedagogyx:pedagogyx_dev@localhost:5432/pedagogyx"
)
JOB_QUEUE_METRICS = os.environ.get("JOB_QUEUE_METRICS", "jobs:talk_ratio")
WORKER_MODE = os.environ.get("WORKER_MODE", "stub")
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "tiny")
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "pedagogyx")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "pedagogyx_dev_minio")
MINIO_BUCKET = os.environ.get("MINIO_BUCKET", "pedagogyx-uploads")
MINIO_SECURE = os.environ.get("MINIO_SECURE", "false").lower() == "true"


def _s3():
    scheme = "https" if MINIO_SECURE else "http"
    return boto3.client(
        "s3",
        endpoint_url=f"{scheme}://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def _db_conn():
    return psycopg2.connect(DATABASE_URL)


def _fetch_chunks(session_id: str) -> list[tuple[int, str]]:
    with _db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT chunk_index, object_key FROM session_chunks
                WHERE session_id = %s ORDER BY chunk_index
                """,
                (session_id,),
            )
            return list(cur.fetchall())


def _fetch_session(session_id: str) -> tuple[str, datetime | None]:
    with _db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT school_id, completed_at FROM sessions WHERE id = %s",
                (session_id,),
            )
            row = cur.fetchone()
            if not row:
                raise ValueError(f"session not found: {session_id}")
            return row[0], row[1]


def _download_chunks(session_id: str, chunks: list[tuple[int, str]]) -> str:
    client = _s3()
    tmp = tempfile.NamedTemporaryFile(suffix=".bin", delete=False)
    path = tmp.name
    tmp.close()
    with open(path, "wb") as out:
        for _idx, key in chunks:
            try:
                obj = client.get_object(Bucket=MINIO_BUCKET, Key=key)
                out.write(obj["Body"].read())
            except ClientError as exc:
                raise RuntimeError(f"minio get {key}: {exc}") from exc
    return path


def _transcribe_stub(session_id: str) -> tuple[str, list[dict], float | None]:
    text = (
        f"[stub transcript session={session_id}] "
        "Teacher explanation segment. Student response segment."
    )
    segments = [
        {"start": 0.0, "end": 30.0, "text": "Teacher explanation segment."},
        {"start": 30.0, "end": 45.0, "text": "Student response segment."},
    ]
    return text, segments, None


def _transcribe_whisper(audio_path: str) -> tuple[str, list[dict], float | None]:
    from faster_whisper import WhisperModel

    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    started = time.perf_counter()
    segments_iter, info = model.transcribe(audio_path, beam_size=1)
    segments = []
    parts = []
    for seg in segments_iter:
        segments.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
        parts.append(seg.text.strip())
    elapsed = time.perf_counter() - started
    duration = info.duration or max((s["end"] for s in segments), default=1.0)
    rtf = elapsed / duration if duration > 0 else None
    return " ".join(parts), segments, rtf


def _save_transcript(session_id: str, text: str, segments: list[dict], rtf: float | None) -> None:
    with _db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO session_transcripts (session_id, language, text, segments_json, rtf)
                VALUES (%s, 'en', %s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE
                SET text = EXCLUDED.text, segments_json = EXCLUDED.segments_json,
                    rtf = EXCLUDED.rtf, processed_at = now()
                """,
                (session_id, text, Json(segments), rtf),
            )
        conn.commit()


def _enqueue_metrics(session_id: str, school_id: str) -> None:
    client = redis.from_url(REDIS_URL, decode_responses=True)
    payload = {
        "job_type": "talk_ratio",
        "session_id": session_id,
        "school_id": school_id,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
    }
    client.rpush(JOB_QUEUE_METRICS, json.dumps(payload))


def process_job(payload: dict) -> None:
    session_id = payload["session_id"]
    school_id = payload.get("school_id")
    if not school_id:
        school_id, _ = _fetch_session(session_id)

    # 1) Get chunks
    chunks = _fetch_chunks(session_id)
    if not chunks:
        return

    audio_path = _download_chunks(session_id, chunks)
    try:
        if WORKER_MODE == "whisper":
            text, segments, rtf = _transcribe_whisper(audio_path)
        else:
            text, segments, rtf = _transcribe_stub(session_id)
    finally:
        try:
            os.unlink(audio_path)
        except OSError:
            pass

    _save_transcript(session_id, text, segments, rtf)
    _enqueue_metrics(session_id, school_id)
    print(
        f"[worker-asr] done session={session_id} mode={WORKER_MODE} rtf={rtf}",
        flush=True,
    )
