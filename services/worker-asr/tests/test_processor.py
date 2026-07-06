import sys; sys.path.append('services/worker-asr')
import unittest
from unittest.mock import patch
from worker.processor import process_job, _transcribe_stub

class TestProcessor(unittest.TestCase):
    def test_transcribe_stub(self):
        text, segments, rtf = _transcribe_stub("test-session-123")

        self.assertEqual(text, "[stub transcript session=test-session-123] Teacher explanation segment. Student response segment.")
        self.assertEqual(segments, [
            {"start": 0.0, "end": 30.0, "text": "Teacher explanation segment."},
            {"start": 30.0, "end": 45.0, "text": "Student response segment."},
        ])
        self.assertIsNone(rtf)

    @patch("worker.processor._fetch_session")
    @patch("worker.processor._fetch_chunks")
    @patch("worker.processor._download_chunks")
    @patch("worker.processor._transcribe_stub")
    @patch("worker.processor._save_transcript")
    @patch("worker.processor._enqueue_metrics")
    @patch("worker.processor.os.unlink")
    def test_process_job_success(
        self,
        mock_unlink,
        mock_enqueue,
        mock_save,
        mock_transcribe,
        mock_download,
        mock_fetch_chunks,
        mock_fetch_session
    ):
        mock_fetch_session.return_value = ("school_1", None)
        mock_fetch_chunks.return_value = [(1, "key1")]
        mock_download.return_value = "/tmp/audio.bin"
        mock_transcribe.return_value = ("stub text", [{"text": "stub"}], 1.0)

        payload = {"session_id": "test-session-123"}
        process_job(payload)

        mock_fetch_session.assert_called_once_with("test-session-123")
        mock_fetch_chunks.assert_called_once_with("test-session-123")
        mock_download.assert_called_once_with("test-session-123", [(1, "key1")])
        mock_transcribe.assert_called_once_with("test-session-123")
        mock_save.assert_called_once_with("test-session-123", "stub text", [{"text": "stub"}], 1.0)
        mock_enqueue.assert_called_once_with("test-session-123", "school_1")
        mock_unlink.assert_called_once_with("/tmp/audio.bin")

    @patch("worker.processor._fetch_chunks")
    @patch("worker.processor._transcribe_stub")
    @patch("worker.processor._save_transcript")
    @patch("worker.processor._enqueue_metrics")
    def test_process_job_no_chunks(
        self,
        mock_enqueue,
        mock_save,
        mock_transcribe,
        mock_fetch_chunks
    ):
        mock_fetch_chunks.return_value = []
        mock_transcribe.return_value = ("stub text", [{"text": "stub"}], 1.0)

        payload = {"session_id": "test-session-123", "school_id": "school_1"}
        process_job(payload)

        mock_fetch_chunks.assert_called_once_with("test-session-123")
        mock_transcribe.assert_called_once_with("test-session-123")
        mock_save.assert_called_once_with("test-session-123", "stub text", [{"text": "stub"}], 1.0)
        mock_enqueue.assert_called_once_with("test-session-123", "school_1")

if __name__ == "__main__":
    unittest.main()
