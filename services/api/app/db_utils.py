import contextlib
import sys
from typing import Any, Generator

import psycopg2
from psycopg2.pool import SimpleConnectionPool

from app.config import settings

_pool = None

def _get_pool():
    global _pool
    if _pool is None:
        # Initialize pool with min 1, max 20 connections
        _pool = SimpleConnectionPool(1, 20, settings.database_url)
    return _pool

@contextlib.contextmanager
def get_conn() -> Generator[Any, None, None]:
    pool = _get_pool()
    conn = pool.getconn()
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
        pool.putconn(conn)
