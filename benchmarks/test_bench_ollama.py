import io
import sys
import unittest
from unittest.mock import patch

import requests
from bench_ollama import main


class TestBenchOllama(unittest.TestCase):
    @patch("bench_ollama.requests.get")
    def test_ollama_not_reachable(self, mock_get):
        mock_get.side_effect = requests.RequestException("Mocked connection error")

        with patch.object(sys, "argv", ["bench_ollama.py"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                exit_code = main()

                self.assertEqual(exit_code, 1)
                output = mock_stdout.getvalue()
                self.assertIn("Ollama not reachable", output)
                self.assertIn("Start Ollama and pull model", output)


if __name__ == "__main__":
    unittest.main()
