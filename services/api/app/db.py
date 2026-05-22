import contextlib
from typing import Any, Generator
from uuid import UUID

import psycopg2
from psycopg2.extras import RealDictCursor

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
            row = cur.fetchone()
            return dict(row)


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
