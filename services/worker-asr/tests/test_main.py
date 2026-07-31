import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from worker.main import main

class TestMain(unittest.TestCase):
    @patch("worker.main.process_job")
    @patch("worker.main.redis.from_url")
    def test_invalid_json_payload(self, mock_from_url, mock_process_job):
        mock_client = MagicMock()
        mock_from_url.return_value = mock_client

        # Return invalid json on the first call, break loop on second call
        mock_client.blpop.side_effect = [
            ("jobs:asr", "invalid { json"),
            Exception("stop loop")
        ]

        captured_stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_stderr

        try:
            main()
        except Exception as e:
            self.assertEqual(str(e), "stop loop")
        finally:
            sys.stderr = old_stderr

        stderr_output = captured_stderr.getvalue()
        self.assertIn("[worker-asr] invalid job: 'invalid { json'", stderr_output)
        mock_process_job.assert_not_called()

if __name__ == "__main__":
    unittest.main()
