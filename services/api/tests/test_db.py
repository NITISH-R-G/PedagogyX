from unittest.mock import patch, MagicMock
from uuid import uuid4
from app.db import get_transcript

def test_get_transcript_found():
    session_id = uuid4()
    mock_row = {"session_id": str(session_id), "text": "Hello world", "language": "en"}

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        mock_cur.fetchone.return_value = mock_row

        result = get_transcript(session_id)

        assert result == mock_row
        mock_cur.execute.assert_called_once_with(
            "SELECT * FROM session_transcripts WHERE session_id = %s",
            (str(session_id),),
        )

def test_get_transcript_not_found():
    session_id = uuid4()

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        mock_cur.fetchone.return_value = None

        result = get_transcript(session_id)

        assert result is None
        mock_cur.execute.assert_called_once_with(
            "SELECT * FROM session_transcripts WHERE session_id = %s",
            (str(session_id),),
        )
