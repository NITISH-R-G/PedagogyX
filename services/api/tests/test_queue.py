import json
from unittest.mock import patch, MagicMock
from uuid import uuid4

from app.queue import enqueue_asr_job, enqueue_talk_ratio_job
from app.config import settings

@patch("app.queue.get_redis")
def test_enqueue_asr_job(mock_get_redis):
    mock_redis_client = MagicMock()
    mock_get_redis.return_value = mock_redis_client

    session_id = uuid4()
    school_id = "test-school-1"

    enqueue_asr_job(session_id, school_id)

    mock_get_redis.assert_called_once()
    mock_redis_client.rpush.assert_called_once()

    args, _ = mock_redis_client.rpush.call_args
    queue_name, payload_str = args

    assert queue_name == settings.job_queue_asr

    payload = json.loads(payload_str)
    assert payload["job_type"] == "asr"
    assert payload["session_id"] == str(session_id)
    assert payload["school_id"] == school_id
    assert "enqueued_at" in payload

@patch("app.queue.get_redis")
def test_enqueue_talk_ratio_job(mock_get_redis):
    mock_redis_client = MagicMock()
    mock_get_redis.return_value = mock_redis_client

    session_id = uuid4()
    school_id = "test-school-2"

    enqueue_talk_ratio_job(session_id, school_id)

    mock_get_redis.assert_called_once()
    mock_redis_client.rpush.assert_called_once()

    args, _ = mock_redis_client.rpush.call_args
    queue_name, payload_str = args

    assert queue_name == settings.job_queue_metrics

    payload = json.loads(payload_str)
    assert payload["job_type"] == "talk_ratio"
    assert payload["session_id"] == str(session_id)
    assert payload["school_id"] == school_id
    assert "enqueued_at" in payload
