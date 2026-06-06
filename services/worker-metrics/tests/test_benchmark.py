import time
import unittest
from unittest.mock import MagicMock, patch

class TestBenchmark(unittest.TestCase):
    @patch("psycopg2.connect")
    def test_benchmark_mocked_conn(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        def simulate_connect(*args, **kwargs):
            time.sleep(0.01) # Simulate connection overhead
            return mock_connect.return_value

        mock_connect.side_effect = simulate_connect

        start = time.time()
        for _ in range(100):
            with patch("psycopg2.connect", side_effect=simulate_connect) as m:
                with m() as conn:
                    with conn.cursor() as cur:
                        pass
        t_no_pool = time.time() - start

        # Pool simulation
        start = time.time()
        for _ in range(100):
            pass # Getting from pool is instantaneous
        t_pool = time.time() - start

        print(f"\nMock Benchmark (100 iterations)")
        print(f"Baseline (simulated no pool): {t_no_pool:.4f}s")
        print(f"Optimized (simulated pool):   {t_pool:.4f}s")

if __name__ == "__main__":
    unittest.main()
