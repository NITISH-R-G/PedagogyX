import contextlib
import sys
from typing import Any, Generator

import psycopg2
from psycopg2 import pool

from app.config import settings

_db_pool: pool.ThreadedConnectionPool | None = None

def init_pool():
    global _db_pool
    if _db_pool is None:
        try:
            # Min 1 connection, max 20 connections in the pool
            _db_pool = pool.ThreadedConnectionPool(
                1, 20, dsn=settings.database_url
            )
        except Exception as e:
            print(f"Failed to initialize database connection pool: {e}", file=sys.stderr)
            raise

def close_pool():
    global _db_pool
    if _db_pool is not None:
        _db_pool.closeall()
        _db_pool = None

@contextlib.contextmanager
def get_conn() -> Generator[Any, None, None]:
    if _db_pool is None:
        raise RuntimeError("Database connection pool is not initialized")

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
