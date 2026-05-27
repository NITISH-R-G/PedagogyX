from unittest.mock import MagicMock, patch
from app.db import insert_session

@patch("app.db.get_conn")
def test_insert_session_happy_path(mock_get_conn):
    mock_conn = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn

    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        "id": "test-id",
        "school_id": "school1",
        "room_id": "room1",
        "teacher_id": "teacher1",
        "status": "active",
        "created_at": "2023-10-10"
    }

    result = insert_session("school1", "room1", "teacher1")

    assert result == {
        "id": "test-id",
        "school_id": "school1",
        "room_id": "room1",
        "teacher_id": "teacher1",
        "status": "active",
        "created_at": "2023-10-10"
    }

    mock_cursor.execute.assert_called_once()
    args, kwargs = mock_cursor.execute.call_args
    assert "INSERT INTO sessions" in args[0]
    assert args[1] == ("school1", "room1", "teacher1")

@patch("app.db.get_conn")
def test_insert_session_none_ids(mock_get_conn):
    mock_conn = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn

    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        "id": "test-id",
        "school_id": "school1",
        "room_id": None,
        "teacher_id": None,
        "status": "active",
        "created_at": "2023-10-10"
    }

    result = insert_session("school1", None, None)

    assert result == {
        "id": "test-id",
        "school_id": "school1",
        "room_id": None,
        "teacher_id": None,
        "status": "active",
        "created_at": "2023-10-10"
    }

    mock_cursor.execute.assert_called_once()
    args, kwargs = mock_cursor.execute.call_args
    assert "INSERT INTO sessions" in args[0]
    assert args[1] == ("school1", None, None)
