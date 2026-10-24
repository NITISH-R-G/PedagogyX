import contextlib
import sys
from typing import Any, Generator

import psycopg2
from psycopg2.pool import ThreadedConnectionPool

from app.config import settings

_db_pool: ThreadedConnectionPool | None = None


def init_db_pool():
    global _db_pool
    if _db_pool is None:
        _db_pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=settings.database_url,
        )


def close_db_pool():
    global _db_pool
    if _db_pool is not None:
        _db_pool.closeall()
        _db_pool = None


@contextlib.contextmanager
def get_conn() -> Generator[Any, None, None]:
    if _db_pool is None:
        raise RuntimeError("Database pool is not initialized")

    conn = _db_pool.getconn()
    try:
        yield conn
        conn.commit()
    except psycopg2.Error as e:
        print(f"Database error in get_conn: {e}", file=sys.stderr)
        conn.rollback()
        raise
    except BaseException as e:
        print(f"Unexpected error in get_conn: {e}", file=sys.stderr)
        conn.rollback()
        raise
    finally:
        _db_pool.putconn(conn)
