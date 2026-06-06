from datetime import datetime, timezone
from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient

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
@patch("app.main.db.list_chunks")
@patch("app.main.db.get_metrics")
@patch("app.main.db.get_transcript")
def test_get_session_happy_path(mock_get_transcript, mock_get_metrics, mock_list_chunks, mock_get_session):
    mock_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    mock_get_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz",
        "status": "completed",
        "created_at": now,
        "completed_at": now,
    }

    mock_list_chunks.return_value = [
        {
            "chunk_index": 0,
            "size_bytes": 1024,
            "content_type": "audio/webm",
            "uploaded_at": now
        }
    ]

    mock_get_metrics.return_value = {
        "teacher_talk_ratio": 0.6,
        "student_talk_ratio": 0.4,
        "metric_confidence": 0.9,
        "preview_ready_at": now,
        "insight_latency_sec": 10
    }

    mock_get_transcript.return_value = {
        "text": "Hello class, today we are learning about testing."
    }

    response = client.get(f"/v1/sessions/{mock_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["school_id"] == "school_123"
    assert data["room_id"] == "room_abc"
    assert data["teacher_id"] == "teacher_xyz"
    assert data["status"] == "completed"
    assert data["created_at"] == now.isoformat()
    assert data["completed_at"] == now.isoformat()

    assert len(data["chunks"]) == 1
    assert data["chunks"][0]["chunk_index"] == 0
    assert data["chunks"][0]["size_bytes"] == 1024
    assert data["chunks"][0]["content_type"] == "audio/webm"
    assert data["chunks"][0]["uploaded_at"] == now.isoformat()

    assert "metrics" in data
    assert data["metrics"]["teacher_talk_ratio"] == 0.6
    assert data["metrics"]["student_talk_ratio"] == 0.4
    assert data["metrics"]["metric_confidence"] == 0.9
    assert data["metrics"]["preview_ready_at"] == now.isoformat()
    assert data["metrics"]["insight_latency_sec"] == 10

    assert "transcript_preview" in data
    assert data["transcript_preview"] == "Hello class, today we are learning about testing."


@patch("app.main.db.get_session")
@patch("app.main.db.list_chunks")
@patch("app.main.db.get_metrics")
@patch("app.main.db.get_transcript")
def test_get_session_minimal_happy_path(mock_get_transcript, mock_get_metrics, mock_list_chunks, mock_get_session):
    mock_id = uuid.uuid4()

    mock_get_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": None,
        "teacher_id": None,
        "status": "active",
        "created_at": None,
        "completed_at": None,
    }

    mock_list_chunks.return_value = []
    mock_get_metrics.return_value = None
    mock_get_transcript.return_value = None

    response = client.get(f"/v1/sessions/{mock_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["school_id"] == "school_123"
    assert data["room_id"] is None
    assert data["teacher_id"] is None
    assert data["status"] == "active"
    assert data["created_at"] is None
    assert data["completed_at"] is None

    assert data["chunks"] == []
    assert "metrics" not in data
    assert "transcript_preview" not in data

@patch("app.main.db.get_session")
def test_get_session_not_found(mock_get_session):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = None

    response = client.get(f"/v1/sessions/{mock_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "session not found"
