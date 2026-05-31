import contextlib
import sys
from typing import Any, Generator

import psycopg2

from app.config import settings


@contextlib.contextmanager
def get_conn() -> Generator[Any, None, None]:
    conn = psycopg2.connect(settings.database_url)
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
        conn.close()
