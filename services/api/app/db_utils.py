import contextlib
from typing import Any, Generator

import psycopg2

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
