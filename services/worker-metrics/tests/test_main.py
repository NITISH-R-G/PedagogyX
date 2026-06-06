import unittest
from unittest.mock import MagicMock, patch
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


class TestComputeTalkRatio(unittest.TestCase):
    def test_compute_talk_ratio_no_row(self):
        mock_cursor = MagicMock()

        mock_cursor.fetchone.return_value = None

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio(mock_cursor, "session123")

        self.assertEqual(teacher, 0.68)
        self.assertEqual(student, 0.32)
        self.assertEqual(confidence, "preview_stub")

    def test_compute_talk_ratio_empty_segments(self):
        mock_cursor = MagicMock()

        mock_cursor.fetchone.return_value = ["[]"]

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio(mock_cursor, "session123")

        self.assertEqual(teacher, 0.68)
        self.assertEqual(student, 0.32)
        self.assertEqual(confidence, "preview_stub")

    def test_compute_talk_ratio_valid_segments(self):
        mock_cursor = MagicMock()

        import json
        segments = [
            {"start": 0.0, "end": 10.0},
            {"start": 10.0, "end": 20.0},
            {"start": 20.0, "end": 35.0}
        ]
        mock_cursor.fetchone.return_value = [json.dumps(segments)]

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio(mock_cursor, "session123")

        # total_dur = 10 + 10 + 15 = 35
        # teacher_dur = 10 + 15 = 25
        # ratio = 25 / 35 = 0.7143
        self.assertEqual(teacher, 0.7143)
        self.assertEqual(student, round(1.0 - 0.7143, 4))
        self.assertEqual(confidence, "preview_heuristic")

    def test_compute_talk_ratio_zero_duration(self):
        mock_cursor = MagicMock()

        import json
        segments = [
            {"start": 10.0, "end": 10.0}
        ]
        mock_cursor.fetchone.return_value = [json.dumps(segments)]

        from worker.main import _compute_talk_ratio
        teacher, student, confidence = _compute_talk_ratio(mock_cursor, "session123")

        self.assertEqual(teacher, 0.68)
        self.assertEqual(student, 0.32)
        self.assertEqual(confidence, "preview_heuristic")

class TestProcessJob(unittest.TestCase):
    @patch("worker.main._insight_latency_sec")
    @patch("worker.main._compute_talk_ratio")
    @patch("worker.main.get_db_pool")
    def test_process_job(self, mock_get_pool, mock_compute, mock_insight):
        mock_compute.return_value = (0.7, 0.3, "high")
        mock_insight.return_value = 10.5

        mock_pool = MagicMock()
        mock_get_pool.return_value = mock_pool

        mock_conn = MagicMock()
        mock_pool.getconn.return_value = mock_conn

        mock_cursor = MagicMock()
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        from datetime import datetime, timezone
        mock_cursor.fetchone.return_value = [datetime(2023, 1, 1, tzinfo=timezone.utc)]

        from worker.main import process_job
        payload = {"session_id": "session123"}
        process_job(payload)

        mock_pool.putconn.assert_called_once_with(mock_conn)
        self.assertEqual(mock_cursor.execute.call_count, 2)
