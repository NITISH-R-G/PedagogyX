from unittest import mock
import pytest

from worker import processor

@mock.patch("worker.processor._fetch_session")
@mock.patch("worker.processor._fetch_chunks")
@mock.patch("worker.processor._transcribe_stub")
@mock.patch("worker.processor._save_transcript")
@mock.patch("worker.processor._enqueue_metrics")
def test_process_job_no_school_id_and_empty_chunks_returns_early(
    mock_enqueue_metrics,
    mock_save_transcript,
    mock_transcribe_stub,
    mock_fetch_chunks,
    mock_fetch_session,
):
    mock_fetch_session.return_value = ("school_456", None)
    mock_fetch_chunks.return_value = []

    payload = {"session_id": "sess_123"}
    processor.process_job(payload)

    mock_fetch_session.assert_called_once_with("sess_123")
    mock_fetch_chunks.assert_called_once_with("sess_123")
    mock_transcribe_stub.assert_not_called()
    mock_save_transcript.assert_not_called()
    mock_enqueue_metrics.assert_not_called()

@mock.patch("worker.processor._fetch_session")
@mock.patch("worker.processor.WORKER_MODE", "stub")
@mock.patch("worker.processor._fetch_chunks")
@mock.patch("worker.processor._download_chunks")
@mock.patch("worker.processor._transcribe_stub")
@mock.patch("worker.processor.os.unlink")
@mock.patch("worker.processor._save_transcript")
@mock.patch("worker.processor._enqueue_metrics")
def test_process_job_no_school_id_with_chunks(
    mock_enqueue_metrics,
    mock_save_transcript,
    mock_unlink,
    mock_transcribe_stub,
    mock_download_chunks,
    mock_fetch_chunks,
    mock_fetch_session,
):
    mock_fetch_session.return_value = ("school_456", None)
    mock_fetch_chunks.return_value = [(0, "chunk1")]
    mock_download_chunks.return_value = "/tmp/fake_audio.bin"
    mock_transcribe_stub.return_value = ("stub text", [], None)

    payload = {"session_id": "sess_123"}
    processor.process_job(payload)

    mock_fetch_session.assert_called_once_with("sess_123")
    mock_fetch_chunks.assert_called_once_with("sess_123")
    mock_download_chunks.assert_called_once_with("sess_123", [(0, "chunk1")])
    mock_transcribe_stub.assert_called_once_with("sess_123")
    mock_unlink.assert_called_once_with("/tmp/fake_audio.bin")
    mock_save_transcript.assert_called_once_with("sess_123", "stub text", [], None)
    mock_enqueue_metrics.assert_called_once_with("sess_123", "school_456")

@mock.patch("worker.processor.WORKER_MODE", "stub")
@mock.patch("worker.processor._fetch_chunks")
@mock.patch("worker.processor._download_chunks")
@mock.patch("worker.processor._transcribe_stub")
@mock.patch("worker.processor.os.unlink")
@mock.patch("worker.processor._save_transcript")
@mock.patch("worker.processor._enqueue_metrics")
def test_process_job_stub_mode(
    mock_enqueue_metrics,
    mock_save_transcript,
    mock_unlink,
    mock_transcribe_stub,
    mock_download_chunks,
    mock_fetch_chunks,
):
    mock_fetch_chunks.return_value = [(0, "chunk1")]
    mock_download_chunks.return_value = "/tmp/fake_audio.bin"
    mock_transcribe_stub.return_value = ("stub text", [], None)

    payload = {"session_id": "sess_123", "school_id": "school_789"}
    processor.process_job(payload)

    mock_fetch_chunks.assert_called_once_with("sess_123")
    mock_download_chunks.assert_called_once_with("sess_123", [(0, "chunk1")])
    mock_transcribe_stub.assert_called_once_with("sess_123")
    mock_unlink.assert_called_once_with("/tmp/fake_audio.bin")
    mock_save_transcript.assert_called_once_with("sess_123", "stub text", [], None)
    mock_enqueue_metrics.assert_called_once_with("sess_123", "school_789")

@mock.patch("worker.processor.WORKER_MODE", "whisper")
@mock.patch("worker.processor._fetch_chunks")
@mock.patch("worker.processor._download_chunks")
@mock.patch("worker.processor._transcribe_whisper")
@mock.patch("worker.processor.os.unlink")
@mock.patch("worker.processor._save_transcript")
@mock.patch("worker.processor._enqueue_metrics")
def test_process_job_whisper_mode(
    mock_enqueue_metrics,
    mock_save_transcript,
    mock_unlink,
    mock_transcribe_whisper,
    mock_download_chunks,
    mock_fetch_chunks,
):
    mock_fetch_chunks.return_value = [(0, "chunk1")]
    mock_download_chunks.return_value = "/tmp/fake_audio.bin"
    mock_transcribe_whisper.return_value = ("whisper text", [{"text": "whisper text"}], 0.5)

    payload = {"session_id": "sess_123", "school_id": "school_789"}
    processor.process_job(payload)

    mock_fetch_chunks.assert_called_once_with("sess_123")
    mock_download_chunks.assert_called_once_with("sess_123", [(0, "chunk1")])
    mock_transcribe_whisper.assert_called_once_with("/tmp/fake_audio.bin")
    mock_unlink.assert_called_once_with("/tmp/fake_audio.bin")
    mock_save_transcript.assert_called_once_with("sess_123", "whisper text", [{"text": "whisper text"}], 0.5)
    mock_enqueue_metrics.assert_called_once_with("sess_123", "school_789")

@mock.patch("worker.processor.WORKER_MODE", "stub")
@mock.patch("worker.processor._fetch_chunks")
@mock.patch("worker.processor._download_chunks")
@mock.patch("worker.processor._transcribe_stub")
@mock.patch("worker.processor.os.unlink")
@mock.patch("worker.processor._save_transcript")
@mock.patch("worker.processor._enqueue_metrics")
def test_process_job_unlink_oserror(
    mock_enqueue_metrics,
    mock_save_transcript,
    mock_unlink,
    mock_transcribe_stub,
    mock_download_chunks,
    mock_fetch_chunks,
):
    mock_fetch_chunks.return_value = [(0, "chunk1")]
    mock_download_chunks.return_value = "/tmp/fake_audio.bin"
    mock_transcribe_stub.return_value = ("stub text", [], None)
    mock_unlink.side_effect = OSError("File not found")

    payload = {"session_id": "sess_123", "school_id": "school_789"}
    # Should not raise exception
    processor.process_job(payload)

    mock_unlink.assert_called_once_with("/tmp/fake_audio.bin")
    mock_save_transcript.assert_called_once_with("sess_123", "stub text", [], None)
