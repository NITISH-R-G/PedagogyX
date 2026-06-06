from unittest.mock import patch
from fastapi.testclient import TestClient
import uuid

from app.main import app

client = TestClient(app)

@patch("app.main.db.insert_session")
def test_create_session(mock_insert_session):
    mock_id = uuid.uuid4()
    mock_insert_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz",
        "status": "active"
    }

    response = client.post("/v1/sessions", json={
        "school_id": "school_123",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["status"] == "active"

    mock_insert_session.assert_called_once_with("school_123", "room_abc", "teacher_xyz")


@patch("app.main.db.insert_session")
def test_create_session_minimal(mock_insert_session):
    mock_id = uuid.uuid4()
    mock_insert_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": None,
        "teacher_id": None,
        "status": "active"
    }

    response = client.post("/v1/sessions", json={
        "school_id": "school_123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["status"] == "active"

    mock_insert_session.assert_called_once_with("school_123", None, None)


def test_create_session_missing_school_id():
    response = client.post("/v1/sessions", json={
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz"
    })

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "school_id"]
    assert data["detail"][0]["type"] == "missing"


def test_create_session_empty_school_id():
    response = client.post("/v1/sessions", json={
        "school_id": "",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz"
    })

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "school_id"]
    assert data["detail"][0]["type"] == "string_too_short"

@patch("app.main.db.get_session")
def test_session_preview_not_found(mock_get_session):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = None

    response = client.get(f"/v1/sessions/{mock_id}/preview")

    assert response.status_code == 404
    assert response.json()["detail"] == "session not found"
    mock_get_session.assert_called_once_with(mock_id)

@patch("app.main.db.get_transcript")
@patch("app.main.db.get_metrics")
@patch("app.main.db.get_session")
def test_session_preview_metrics_pending(mock_get_session, mock_get_metrics, mock_get_transcript):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = {"status": "active"}
    mock_get_metrics.return_value = None
    mock_get_transcript.return_value = None

    response = client.get(f"/v1/sessions/{mock_id}/preview")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["status"] == "active"
    assert data["preview_ready"] is False
    assert data["message"] == "metrics pending"

    mock_get_session.assert_called_once_with(mock_id)
    mock_get_metrics.assert_called_once_with(mock_id)
    mock_get_transcript.assert_called_once_with(mock_id)

@patch("app.main.db.get_transcript")
@patch("app.main.db.get_metrics")
@patch("app.main.db.get_session")
def test_session_preview_metrics_no_transcript(mock_get_session, mock_get_metrics, mock_get_transcript):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = {"status": "completed"}
    mock_get_metrics.return_value = {
        "preview_ready_at": "2023-01-01T00:00:00Z",
        "teacher_talk_ratio": 0.6,
        "student_talk_ratio": 0.4,
        "metric_confidence": 0.9,
        "insight_latency_sec": 1.5,
    }
    mock_get_transcript.return_value = None

    response = client.get(f"/v1/sessions/{mock_id}/preview")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["status"] == "completed"
    assert data["preview_ready"] is True
    assert data["teacher_talk_ratio"] == 0.6
    assert data["student_talk_ratio"] == 0.4
    assert data["metric_confidence"] == 0.9
    assert data["insight_latency_sec"] == 1.5
    assert data["transcript_excerpt"] is None

@patch("app.main.db.get_transcript")
@patch("app.main.db.get_metrics")
@patch("app.main.db.get_session")
def test_session_preview_full(mock_get_session, mock_get_metrics, mock_get_transcript):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = {"status": "completed"}
    mock_get_metrics.return_value = {
        "preview_ready_at": "2023-01-01T00:00:00Z",
        "teacher_talk_ratio": 0.6,
        "student_talk_ratio": 0.4,
        "metric_confidence": 0.9,
        "insight_latency_sec": 1.5,
    }
    long_text = "This is a very long transcript text. " * 20
    mock_get_transcript.return_value = {"text": long_text}

    response = client.get(f"/v1/sessions/{mock_id}/preview")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["status"] == "completed"
    assert data["preview_ready"] is True
    assert data["teacher_talk_ratio"] == 0.6
    assert data["transcript_excerpt"] == long_text[:300]
