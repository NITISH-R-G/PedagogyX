import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from worker.main import main

class TestMain(unittest.TestCase):
    @patch("worker.main.redis.from_url")
    @patch("worker.main.process_job")
    def test_invalid_json_payload(self, mock_process_job, mock_redis_from_url):
        mock_client = MagicMock()
        mock_redis_from_url.return_value = mock_client

        mock_client.blpop.side_effect = [
            ("jobs:asr", "invalid-json"),
            KeyboardInterrupt()
        ]

        captured_stdout = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_stdout
        try:
            with self.assertRaises(KeyboardInterrupt):
                main()
        finally:
            sys.stdout = old_stdout

        stdout_output = captured_stdout.getvalue()
        self.assertIn("worker-asr: invalid json payload, skipping", stdout_output)
        mock_process_job.assert_not_called()

if __name__ == '__main__':
    unittest.main()
