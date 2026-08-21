import json
import os
import subprocess
import tempfile
import time
from datetime import UTC, datetime

import boto3

from worker.config import (
    DATABASE_URL,
    JOB_QUEUE_METRICS,
    S3_BUCKET_NAME,
    S3_ENDPOINT,
)


def _db_conn():
    import psycopg2

    return psycopg2.connect(DATABASE_URL)


def _s3():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )


def _transcribe_stub(audio_path: str) -> dict:
    # MVP Stub: Normally we'd call Whisper/Faster-Whisper here
    time.sleep(2.0)
    return {
        "text": f"Stub transcript for {os.path.basename(audio_path)}",
        "segments": [{"start": 0.0, "end": 1.0, "text": "stub"}],
        "language": "en",
    }


def _fetch_chunks(session_id: str) -> list[tuple[int, str]]:
    with _db_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT chunk_index, object_key FROM session_chunks
            WHERE session_id = %s ORDER BY chunk_index
            """,
            (session_id,),
        )
        return list(cur.fetchall())


def _fetch_session(session_id: str) -> tuple[str, datetime | None]:
    with _db_conn() as conn, conn.cursor() as cur:
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

    try:
        with open(path, "wb") as f:
            for idx, key in chunks:
                resp = client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
                f.write(resp["Body"].read())
        return path
    except Exception as exc:
        if os.path.exists(path):
            os.remove(path)
        raise RuntimeError(f"Failed to download chunks: {exc}") from exc


def _extract_audio(bin_path: str) -> str:
    out_path = bin_path + ".wav"
    # MVP: Assuming binary is just raw audio for now, or use ffmpeg to convert
    # For dat-session simulation, it's actually raw wav
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            bin_path,
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            out_path,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if not os.path.exists(out_path):
        # fallback: just copy
        subprocess.run(["cp", bin_path, out_path], check=True)
    return out_path


def _save_transcript(session_id: str, transcript: dict) -> None:
    from psycopg2.extras import Json

    with _db_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO transcripts (session_id, text, segments, language)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (session_id) DO UPDATE SET
                text = EXCLUDED.text,
                segments = EXCLUDED.segments,
                language = EXCLUDED.language,
                updated_at = NOW()
            """,
            (
                session_id,
                transcript.get("text", ""),
                Json(transcript.get("segments", [])),
                transcript.get("language", "en"),
            ),
        )
        conn.commit()


def process_job(payload: dict) -> None:
    session_id = payload["session_id"]
    school_id, _completed_at = _fetch_session(session_id)

    chunks = _fetch_chunks(session_id)
    if not chunks:
        print(f"[{session_id}] No chunks found. Skipping ASR.")
        return

    bin_path = _download_chunks(session_id, chunks)
    audio_path = _extract_audio(bin_path)

    try:
        transcript = _transcribe_stub(audio_path)
        _save_transcript(session_id, transcript)
        print(f"[{session_id}] ASR complete. Enqueuing metrics job.")
        _enqueue_metrics(session_id, school_id)
    finally:
        if os.path.exists(bin_path):
            os.remove(bin_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)


def _enqueue_metrics(session_id: str, school_id: str) -> None:
    import redis

    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    client = redis.from_url(redis_url)

    payload = {
        "job_type": "calculate_metrics",
        "session_id": session_id,
        "school_id": school_id,
        "enqueued_at": datetime.now(UTC).isoformat(),
    }
    client.rpush(JOB_QUEUE_METRICS, json.dumps(payload))
