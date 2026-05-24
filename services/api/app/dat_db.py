"""DAT session persistence (Meta Wearables DAT lifecycle mirror)."""

import contextlib
from typing import Any, Generator
from uuid import UUID

import psycopg2
from psycopg2.extras import Json, RealDictCursor

from app.config import settings

# Allowed transitions (server-enforced subset)
DAT_SESSION_TRANSITIONS: dict[str, set[str]] = {
    "IDLE": {"STARTING"},
    "STARTING": {"STARTED", "STOPPED"},
    "STARTED": {"PAUSED", "STOPPING", "STREAMING"},
    "PAUSED": {"STARTED", "STOPPING"},
    "STREAMING": {"STARTED", "STOPPING", "PAUSED"},
    "STOPPING": {"STOPPED"},
    "STOPPED": set(),
}

STREAM_TRANSITIONS: dict[str, set[str]] = {
    "STOPPED": {"STARTING"},
    "STARTING": {"STARTED", "STREAMING", "STOPPED"},
    "STARTED": {"STREAMING", "STOPPING", "STOPPED"},
    "STREAMING": {"STOPPING", "STOPPED"},
    "STOPPING": {"STOPPED"},
}


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


def create_dat_session(
    school_id: str,
    room_id: str | None,
    teacher_id: str | None,
    device_label: str | None,
) -> dict:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO dat_sessions (school_id, room_id, teacher_id, device_label, state, stream_state)
                VALUES (%s, %s, %s, %s, 'IDLE', 'STOPPED')
                RETURNING *
                """,
                (school_id, room_id, teacher_id, device_label),
            )
            return dict(cur.fetchone())


def get_dat_session(dat_id: UUID) -> dict | None:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM dat_sessions WHERE id = %s", (str(dat_id),))
            row = cur.fetchone()
            return dict(row) if row else None


def link_pedagogy_session(dat_id: UUID, pedagogy_session_id: UUID) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE dat_sessions
                SET pedagogy_session_id = %s, updated_at = now()
                WHERE id = %s
                """,
                (str(pedagogy_session_id), str(dat_id)),
            )


def append_event(
    dat_id: UUID,
    event_type: str,
    from_state: str | None,
    to_state: str | None,
    detail: dict | None = None,
) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO dat_session_events (dat_session_id, event_type, from_state, to_state, detail)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (str(dat_id), event_type, from_state, to_state, Json(detail or {})),
            )


def transition_session_state(dat_id: UUID, new_state: str, event_type: str, detail: dict | None) -> dict:
    row = get_dat_session(dat_id)
    if not row:
        raise ValueError("dat session not found")
    current = row["state"]
    allowed = DAT_SESSION_TRANSITIONS.get(current, set())
    if new_state not in allowed and new_state != current:
        raise ValueError(f"invalid session transition {current} -> {new_state}")
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE dat_sessions SET state = %s, updated_at = now()
                WHERE id = %s RETURNING *
                """,
                (new_state, str(dat_id)),
            )
            updated = dict(cur.fetchone())
    append_event(dat_id, event_type, current, new_state, detail)
    return updated


def transition_stream_state(dat_id: UUID, new_state: str, event_type: str, detail: dict | None) -> dict:
    row = get_dat_session(dat_id)
    if not row:
        raise ValueError("dat session not found")
    if row["state"] not in ("STARTED", "STREAMING", "PAUSED") and new_state not in ("STOPPED",):
        raise ValueError("stream requires session STARTED (or STREAMING/PAUSED)")
    current = row["stream_state"]
    allowed = STREAM_TRANSITIONS.get(current, set())
    if new_state not in allowed and new_state != current:
        raise ValueError(f"invalid stream transition {current} -> {new_state}")
    session_state = row["state"]
    if new_state == "STREAMING" and session_state == "STARTED":
        session_state = "STREAMING"
    elif new_state == "STOPPED" and session_state == "STREAMING":
        session_state = "STARTED"
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE dat_sessions
                SET stream_state = %s, state = %s, updated_at = now()
                WHERE id = %s RETURNING *
                """,
                (new_state, session_state, str(dat_id)),
            )
            updated = dict(cur.fetchone())
    append_event(dat_id, event_type, current, new_state, detail)
    return updated


def list_events(dat_id: UUID, limit: int = 50) -> list[dict]:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT event_type, from_state, to_state, detail, created_at
                FROM dat_session_events
                WHERE dat_session_id = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (str(dat_id), limit),
            )
            return [dict(r) for r in cur.fetchall()]
