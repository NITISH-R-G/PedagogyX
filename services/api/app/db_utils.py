import contextlib
import sys
from typing import Any, Generator

import psycopg2
from psycopg2 import pool

from app.config import settings

_db_pool = None

def get_pool():
    global _db_pool
    if _db_pool is None:
        _db_pool = pool.ThreadedConnectionPool(1, 10, settings.database_url)
    return _db_pool

@contextlib.contextmanager
def get_conn() -> Generator[Any, None, None]:
    db_pool = get_pool()
    conn = db_pool.getconn()
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
        db_pool.putconn(conn)
