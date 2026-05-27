import unittest
from unittest.mock import MagicMock, patch
from worker.main import _insight_latency_sec


class TestInsightLatencySec(unittest.TestCase):
    @patch("worker.main.psycopg2.connect")
    def test_insight_latency_sec_success(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        # Setup the context managers
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Setup the query result
        mock_cursor.fetchone.return_value = [123.45]

        session_id = "test-session-123"

        # Act
        result = _insight_latency_sec(session_id)

        # Assert
        self.assertEqual(result, 123.45)
        mock_cursor.execute.assert_called_once()
        self.assertIn("SELECT EXTRACT(EPOCH FROM", mock_cursor.execute.call_args[0][0])
        self.assertEqual(mock_cursor.execute.call_args[0][1], (session_id,))

    @patch("worker.main.psycopg2.connect")
    def test_insight_latency_sec_missing_row(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Setup the query result to return None (no row found)
        mock_cursor.fetchone.return_value = None

        # Act
        result = _insight_latency_sec("test-session-123")

        # Assert
        self.assertIsNone(result)

    @patch("worker.main.psycopg2.connect")
    def test_insight_latency_sec_null_value(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Setup the query result to return a row, but the value is None
        mock_cursor.fetchone.return_value = [None]

        # Act
        result = _insight_latency_sec("test-session-123")

        # Assert
        self.assertIsNone(result)
