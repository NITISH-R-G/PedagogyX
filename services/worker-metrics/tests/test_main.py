import unittest
from unittest.mock import MagicMock
from worker.main import _insight_latency_sec


class TestInsightLatencySec(unittest.TestCase):
    def test_insight_latency_sec_success(self):
        # Arrange
        mock_cursor = MagicMock()

        # Setup the query result
        mock_cursor.fetchone.return_value = [123.45]

        session_id = "test-session-123"

        # Act
        result = _insight_latency_sec(mock_cursor, session_id)

        # Assert
        self.assertEqual(result, 123.45)
        mock_cursor.execute.assert_called_once()
        self.assertIn("SELECT EXTRACT(EPOCH FROM", mock_cursor.execute.call_args[0][0])
        self.assertEqual(mock_cursor.execute.call_args[0][1], (session_id,))

    def test_insight_latency_sec_missing_row(self):
        # Arrange
        mock_cursor = MagicMock()

        # Setup the query result to return None (no row found)
        mock_cursor.fetchone.return_value = None

        # Act
        result = _insight_latency_sec(mock_cursor, "test-session-123")

        # Assert
        self.assertIsNone(result)

    def test_insight_latency_sec_null_value(self):
        # Arrange
        mock_cursor = MagicMock()

        # Setup the query result to return a row, but the value is None
        mock_cursor.fetchone.return_value = [None]

        # Act
        result = _insight_latency_sec(mock_cursor, "test-session-123")

        # Assert
        self.assertIsNone(result)
