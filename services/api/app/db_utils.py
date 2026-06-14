import contextlib
import sys
from typing import Any, Generator

import psycopg2
from psycopg2 import pool

from app.config import settings

_db_pool: pool.ThreadedConnectionPool | None = None

def init_pool(minconn: int = 1, maxconn: int = 10) -> None:
    global _db_pool
    if _db_pool is None:
        _db_pool = pool.ThreadedConnectionPool(minconn, maxconn, settings.database_url)

def close_pool() -> None:
    global _db_pool
    if _db_pool is not None:
        _db_pool.closeall()
        _db_pool = None

@contextlib.contextmanager
def get_conn() -> Generator[Any, None, None]:
    if _db_pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_pool() first.")

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
