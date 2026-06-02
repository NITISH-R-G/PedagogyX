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


class TestComputeTalkRatio(unittest.TestCase):
    @patch("worker.main.psycopg2.connect")
    def test_compute_talk_ratio_no_row(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = None

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio("session123")

        self.assertEqual(teacher, 0.68)
        self.assertEqual(student, 0.32)
        self.assertEqual(confidence, "preview_stub")

    @patch("worker.main.psycopg2.connect")
    def test_compute_talk_ratio_empty_segments(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ["[]"]

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio("session123")

        self.assertEqual(teacher, 0.68)
        self.assertEqual(student, 0.32)
        self.assertEqual(confidence, "preview_stub")

    @patch("worker.main.psycopg2.connect")
    def test_compute_talk_ratio_valid_segments(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        import json
        segments = [
            {"start": 0.0, "end": 10.0},
            {"start": 10.0, "end": 20.0},
            {"start": 20.0, "end": 35.0}
        ]
        mock_cursor.fetchone.return_value = [json.dumps(segments)]

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio("session123")

        # total_dur = 10 + 10 + 15 = 35
        # teacher_dur = 10 + 15 = 25
        # ratio = 25 / 35 = 0.7143
        self.assertEqual(teacher, 0.7143)
        self.assertEqual(student, round(1.0 - 0.7143, 4))
        self.assertEqual(confidence, "preview_heuristic")

    @patch("worker.main.psycopg2.connect")
    def test_compute_talk_ratio_zero_duration(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        import json
        segments = [
            {"start": 10.0, "end": 10.0}
        ]
        mock_cursor.fetchone.return_value = [json.dumps(segments)]

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio("session123")

        self.assertEqual(teacher, 0.68)
        self.assertEqual(student, 0.32)
        self.assertEqual(confidence, "preview_heuristic")

class TestProcessJob(unittest.TestCase):
    @patch("worker.main._insight_latency_sec")
    @patch("worker.main._compute_talk_ratio")
    @patch("worker.main.psycopg2.connect")
    def test_process_job(self, mock_connect, mock_compute, mock_insight):
        mock_compute.return_value = (0.7, 0.3, "high")
        mock_insight.return_value = 10.5

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        from datetime import datetime, timezone
        mock_cursor.fetchone.return_value = [datetime(2023, 1, 1, tzinfo=timezone.utc)]

        from worker.main import process_job
        payload = {"session_id": "session123"}
        process_job(payload)

        mock_conn.commit.assert_called_once()
        self.assertEqual(mock_cursor.execute.call_count, 2)
