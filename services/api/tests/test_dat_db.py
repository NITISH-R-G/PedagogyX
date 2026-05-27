import pytest
from unittest.mock import MagicMock, patch

from app.dat_db import create_dat_session, get_conn


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
