import contextlib
from datetime import datetime, timezone
from typing import Any, Generator
from uuid import UUID

import psycopg2
from psycopg2.extras import RealDictCursor, Json

from app.config import settings


@contextlib.contextmanager
def get_conn() -> Generator[Any, None, None]:
    conn = psycopg2.connect(settings.database_url)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def insert_session(school_id: str, room_id: str | None, teacher_id: str | None) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO sessions (school_id, room_id, teacher_id, status)
                VALUES (%s, %s, %s, 'active')
                RETURNING id, school_id, room_id, teacher_id, status, created_at
                """,
                (school_id, room_id, teacher_id),
            )
            return dict(cur.fetchone())


def complete_session(session_id: UUID) -> dict | None:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE sessions
                SET status = 'completed', completed_at = now()
                WHERE id = %s
                RETURNING id, school_id, room_id, teacher_id, status, created_at, completed_at
                """,
                (str(session_id),),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def get_session(session_id: UUID) -> dict | None:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM sessions WHERE id = %s", (str(session_id),))
            row = cur.fetchone()
            return dict(row) if row else None


def insert_chunk(
    session_id: UUID, chunk_index: int, object_key: str, size_bytes: int, content_type: str | None
) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO session_chunks (session_id, chunk_index, object_key, size_bytes, content_type)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (session_id, chunk_index) DO UPDATE
                SET object_key = EXCLUDED.object_key,
                    size_bytes = EXCLUDED.size_bytes,
                    content_type = EXCLUDED.content_type,
                    uploaded_at = now()
                RETURNING session_id, chunk_index, object_key, size_bytes, content_type, uploaded_at
                """,
                (str(session_id), chunk_index, object_key, size_bytes, content_type),
            )
            return dict(cur.fetchone())


def list_chunks(session_id: UUID) -> list[dict]:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT chunk_index, object_key, size_bytes, content_type, uploaded_at
                FROM session_chunks WHERE session_id = %s ORDER BY chunk_index
                """,
                (str(session_id),),
            )
            return [dict(r) for r in cur.fetchall()]


def count_chunks(session_id: UUID) -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM session_chunks WHERE session_id = %s",
                (str(session_id),),
            )
            return int(cur.fetchone()[0])


def save_transcript(
    session_id: UUID,
    text: str,
    segments: list[dict],
    rtf: float | None,
    language: str = "en",
) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO session_transcripts (session_id, language, text, segments_json, rtf)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE
                SET text = EXCLUDED.text,
                    segments_json = EXCLUDED.segments_json,
                    rtf = EXCLUDED.rtf,
                    processed_at = now()
                """,
                (str(session_id), language, text, Json(segments), rtf),
            )


def get_transcript(session_id: UUID) -> dict | None:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM session_transcripts WHERE session_id = %s",
                (str(session_id),),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def save_metrics(
    session_id: UUID,
    teacher_ratio: float,
    student_ratio: float,
    confidence: str,
    insight_latency_sec: float | None,
) -> None:
    now = datetime.now(timezone.utc)
    with get_conn() as conn:
        with conn.cursor() as cur:
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
                (
                    str(session_id),
                    teacher_ratio,
                    student_ratio,
                    confidence,
                    now,
                    insight_latency_sec,
                    now,
                ),
            )


def get_metrics(session_id: UUID) -> dict | None:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM session_metrics WHERE session_id = %s",
                (str(session_id),),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def school_overview(school_id: str) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT COUNT(DISTINCT room_id) FILTER (WHERE room_id IS NOT NULL) AS rooms_observed,
                       COUNT(*) AS sessions_total,
                       COUNT(*) FILTER (WHERE status = 'completed') AS sessions_completed,
                       COUNT(*) FILTER (
                           WHERE status = 'completed' AND completed_at > now() - interval '7 days'
                       ) AS sessions_week
                FROM sessions WHERE school_id = %s
                """,
                (school_id,),
            )
            counts = dict(cur.fetchone())

            cur.execute(
                """
                SELECT s.id, s.room_id, s.teacher_id, s.status, s.created_at, s.completed_at,
                       m.teacher_talk_ratio, m.student_talk_ratio, m.preview_ready_at,
                       m.insight_latency_sec, m.metric_confidence
                FROM sessions s
                LEFT JOIN session_metrics m ON m.session_id = s.id
                WHERE s.school_id = %s
                ORDER BY s.created_at DESC
                LIMIT 20
                """,
                (school_id,),
            )
            recent = [_serialize_overview_row(dict(r)) for r in cur.fetchall()]

            cur.execute(
                """
                SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY insight_latency_sec)
                FROM session_metrics m
                JOIN sessions s ON s.id = m.session_id
                WHERE s.school_id = %s AND m.insight_latency_sec IS NOT NULL
                """,
                (school_id,),
            )
            median_row = cur.fetchone()
            median_latency = float(median_row["percentile_cont"]) if median_row["percentile_cont"] else None

    rooms_target = int(settings.overview_rooms_target)
    rooms_observed = int(counts["rooms_observed"] or 0)
    coverage_pct = round(100.0 * rooms_observed / rooms_target, 1) if rooms_target else 0.0

    return {
        "school_id": school_id,
        "m_a_coverage": {
            "rooms_observed": rooms_observed,
            "rooms_target": rooms_target,
            "coverage_pct": min(100.0, coverage_pct),
        },
        "m_b_median_insight_sec": median_latency,
        "sessions_total": int(counts["sessions_total"] or 0),
        "sessions_completed": int(counts["sessions_completed"] or 0),
        "sessions_week": int(counts["sessions_week"] or 0),
        "recent_sessions": recent,
    }


def _serialize_overview_row(row: dict) -> dict:
    out = {
        "id": str(row["id"]),
        "room_id": row.get("room_id"),
        "teacher_id": row.get("teacher_id"),
        "status": row["status"],
        "teacher_talk_ratio": row.get("teacher_talk_ratio"),
        "student_talk_ratio": row.get("student_talk_ratio"),
        "insight_latency_sec": row.get("insight_latency_sec"),
        "metric_confidence": row.get("metric_confidence"),
    }
    if row.get("created_at"):
        out["created_at"] = row["created_at"].isoformat()
    if row.get("completed_at"):
        out["completed_at"] = row["completed_at"].isoformat()
    if row.get("preview_ready_at"):
        out["preview_ready_at"] = row["preview_ready_at"].isoformat()
    return out
