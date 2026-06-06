import pytest
from unittest.mock import MagicMock, patch

from app.dat_db import create_dat_session
from app.db_utils import get_conn


@patch("app.db_utils.psycopg2.connect")
def test_get_conn_rollback_on_error(mock_connect):
    """
    Directly test the get_conn context manager to ensure that an exception
    raised within its block causes a rollback, closes the connection,
    and re-raises the exception.
    """
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    with pytest.raises(Exception, match="DB error"):
        with get_conn():
            raise Exception("DB error")

    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_conn.commit.assert_not_called()


@patch("app.db_utils.psycopg2.connect")
def test_create_dat_session_rollback_on_error(mock_connect):
    """
    Test that if an exception occurs during db operations inside get_conn,
    the connection rolls back, does not commit, and the exception is re-raised.
    """
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    # Setup the mock for `with conn.cursor(...) as cur:`
    mock_cursor_ctx = MagicMock()
    mock_conn.cursor.return_value = mock_cursor_ctx

    mock_cur = MagicMock()
    mock_cursor_ctx.__enter__.return_value = mock_cur

    # Force an exception when cur.execute is called
    mock_cur.execute.side_effect = Exception("DB execute error")

    with pytest.raises(Exception, match="DB execute error"):
        create_dat_session("school_1", "room_1", "teacher_1", "device_1")

    # Assert rollback and close were called, but not commit
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_conn.commit.assert_not_called()


@patch("app.db_utils.psycopg2.connect")
def test_create_dat_session_success(mock_connect):
    """
    Test the happy path of create_dat_session to ensure it executes the query
    and returns the inserted row dictionary.
    """
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

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

    # Assert commit and close were called, but not rollback
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_cur.execute.assert_called_once()

@patch("app.db_utils.psycopg2.connect")
def test_link_pedagogy_session_success(mock_connect):
    """
    Test the happy path of link_pedagogy_session to ensure it executes the
    correct UPDATE query.
    """
    from app.dat_db import link_pedagogy_session
    import uuid

    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    # Setup the mock for `with conn.cursor() as cur:`
    mock_cursor_ctx = MagicMock()
    mock_conn.cursor.return_value = mock_cursor_ctx

    mock_cur = MagicMock()
    mock_cursor_ctx.__enter__.return_value = mock_cur

    dat_id = uuid.uuid4()
    pedagogy_session_id = uuid.uuid4()

    link_pedagogy_session(dat_id, pedagogy_session_id)

    # Assert execute was called correctly
    mock_cur.execute.assert_called_once()
    args, kwargs = mock_cur.execute.call_args
    assert "UPDATE dat_sessions" in args[0]
    assert "SET pedagogy_session_id = %s, updated_at = now()" in args[0]
    assert "WHERE id = %s" in args[0]
    assert args[1] == (str(pedagogy_session_id), str(dat_id))

    # Assert commit and close were called, but not rollback
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_conn.rollback.assert_not_called()


@patch("app.db_utils.psycopg2.connect")
def test_link_pedagogy_session_rollback_on_error(mock_connect):
    """
    Test that an exception during link_pedagogy_session causes a rollback.
    """
    from app.dat_db import link_pedagogy_session
    import uuid

    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    mock_cursor_ctx = MagicMock()
    mock_conn.cursor.return_value = mock_cursor_ctx

    mock_cur = MagicMock()
    mock_cursor_ctx.__enter__.return_value = mock_cur

    mock_cur.execute.side_effect = Exception("DB update error")

    dat_id = uuid.uuid4()
    pedagogy_session_id = uuid.uuid4()

    with pytest.raises(Exception, match="DB update error"):
        link_pedagogy_session(dat_id, pedagogy_session_id)

    # Assert rollback and close were called, but not commit
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
    mock_conn.commit.assert_not_called()
