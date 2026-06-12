import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.dat_db import create_dat_session, get_dat_session
from app.db_utils import get_conn


def test_get_conn_rollback_on_psycopg2_error(capsys, monkeypatch):
    """
    Directly test the get_conn context manager to ensure that a psycopg2.Error
    raised within its block causes a rollback, closes the connection,
    prints to stderr, and re-raises the exception.
    """
    import psycopg2
    from app import db_utils

    mock_pool = MagicMock()
    mock_conn = MagicMock()
    mock_pool.getconn.return_value = mock_conn

    # Set the global pool mock directly
    monkeypatch.setattr(db_utils, "_db_pool", mock_pool)

    with pytest.raises(psycopg2.Error, match="DB psycopg2 error"):
        with get_conn():
            raise psycopg2.Error("DB psycopg2 error")

    mock_conn.rollback.assert_called_once()
    mock_conn.commit.assert_not_called()
    mock_pool.putconn.assert_called_once_with(mock_conn)

    captured = capsys.readouterr()
    assert "Database error in get_conn: DB psycopg2 error" in captured.err


def test_get_conn_rollback_on_error(capsys, monkeypatch):
    """
    Directly test the get_conn context manager to ensure that an exception
    raised within its block causes a rollback, closes the connection,
    prints to stderr, and re-raises the exception.
    """
    from app import db_utils

    mock_pool = MagicMock()
    mock_conn = MagicMock()
    mock_pool.getconn.return_value = mock_conn

    monkeypatch.setattr(db_utils, "_db_pool", mock_pool)

    with pytest.raises(Exception, match="DB error"):
        with get_conn():
            raise Exception("DB error")

    mock_conn.rollback.assert_called_once()
    mock_conn.commit.assert_not_called()
    mock_pool.putconn.assert_called_once_with(mock_conn)

    captured = capsys.readouterr()
    assert "Unexpected error in get_conn: DB error" in captured.err


def test_create_dat_session_rollback_on_error(monkeypatch):
    """
    Test that if an exception occurs during db operations inside get_conn,
    the connection rolls back, does not commit, and the exception is re-raised.
    """
    from app import db_utils

    mock_pool = MagicMock()
    mock_conn = MagicMock()
    mock_pool.getconn.return_value = mock_conn
    monkeypatch.setattr(db_utils, "_db_pool", mock_pool)

    # Setup the mock for `with conn.cursor(...) as cur:`
    mock_cursor_ctx = MagicMock()
    mock_conn.cursor.return_value = mock_cursor_ctx

    mock_cur = MagicMock()
    mock_cursor_ctx.__enter__.return_value = mock_cur

    # Force an exception when cur.execute is called
    mock_cur.execute.side_effect = Exception("DB execute error")

    with pytest.raises(Exception, match="DB execute error"):
        create_dat_session("school_1", "room_1", "teacher_1", "device_1")

    # Assert rollback was called, but not commit
    mock_conn.rollback.assert_called_once()
    mock_conn.commit.assert_not_called()
    mock_pool.putconn.assert_called_once_with(mock_conn)


def test_create_dat_session_success(monkeypatch):
    """
    Test the happy path of create_dat_session to ensure it executes the query
    and returns the inserted row dictionary.
    """
    from app import db_utils

    mock_pool = MagicMock()
    mock_conn = MagicMock()
    mock_pool.getconn.return_value = mock_conn
    monkeypatch.setattr(db_utils, "_db_pool", mock_pool)

    # Setup the mock for `with conn.cursor(...) as cur:`
    mock_cursor_ctx = MagicMock()
    mock_conn.cursor.return_value = mock_cursor_ctx

    mock_cur = MagicMock()
    mock_cursor_ctx.__enter__.return_value = mock_cur

    expected_row = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
        "device_label": "device_1",
        "state": "IDLE",
        "stream_state": "STOPPED",
    }
    mock_cur.fetchone.return_value = expected_row

    result = create_dat_session("school_1", "room_1", "teacher_1", "device_1")

    assert result == expected_row

    # Assert commit was called, but not rollback
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_cur.execute.assert_called_once()
    mock_pool.putconn.assert_called_once_with(mock_conn)


def test_get_dat_session_not_found(monkeypatch):
    """
    Test that get_dat_session returns None when no row is found.
    """
    from app import db_utils

    mock_pool = MagicMock()
    mock_conn = MagicMock()
    mock_pool.getconn.return_value = mock_conn
    monkeypatch.setattr(db_utils, "_db_pool", mock_pool)

    # Setup the mock for `with conn.cursor(...) as cur:`
    mock_cursor_ctx = MagicMock()
    mock_conn.cursor.return_value = mock_cursor_ctx

    mock_cur = MagicMock()
    mock_cursor_ctx.__enter__.return_value = mock_cur

    # Simulate no row found
    mock_cur.fetchone.return_value = None

    test_uuid = uuid4()
    result = get_dat_session(test_uuid)

    assert result is None
    mock_cur.execute.assert_called_once_with(
        "SELECT * FROM dat_sessions WHERE id = %s", (str(test_uuid),)
    )
    mock_pool.putconn.assert_called_once_with(mock_conn)


def test_get_dat_session_success(monkeypatch):
    """
    Test the happy path of get_dat_session returning a row.
    """
    from app import db_utils

    mock_pool = MagicMock()
    mock_conn = MagicMock()
    mock_pool.getconn.return_value = mock_conn
    monkeypatch.setattr(db_utils, "_db_pool", mock_pool)

    # Setup the mock for `with conn.cursor(...) as cur:`
    mock_cursor_ctx = MagicMock()
    mock_conn.cursor.return_value = mock_cursor_ctx

    mock_cur = MagicMock()
    mock_cursor_ctx.__enter__.return_value = mock_cur

    expected_row = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "school_id": "school_1",
        "state": "IDLE",
    }
    mock_cur.fetchone.return_value = expected_row

    test_uuid = uuid4()
    result = get_dat_session(test_uuid)

    assert result == expected_row
    mock_cur.execute.assert_called_once_with(
        "SELECT * FROM dat_sessions WHERE id = %s", (str(test_uuid),)
    )
    mock_pool.putconn.assert_called_once_with(mock_conn)
