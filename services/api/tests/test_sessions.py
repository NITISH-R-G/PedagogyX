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
def test_complete_session_not_found(mock_get_session):
    mock_get_session.return_value = None
    session_id = uuid.uuid4()

    response = client.post(f"/v1/sessions/{session_id}/complete")

    assert response.status_code == 404
    assert response.json()["detail"] == "session not found"
    mock_get_session.assert_called_once_with(session_id)


@patch("app.main.db.get_session")
def test_complete_session_already_completed(mock_get_session):
    session_id = uuid.uuid4()
    mock_get_session.return_value = {
        "id": session_id,
        "status": "completed"
    }

    response = client.post(f"/v1/sessions/{session_id}/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["job_enqueued"] == "asr"
    assert data["note"] == "already completed"
    mock_get_session.assert_called_once_with(session_id)


@patch("app.main.db.count_chunks")
@patch("app.main.db.get_session")
def test_complete_session_zero_chunks(mock_get_session, mock_count_chunks):
    session_id = uuid.uuid4()
    mock_get_session.return_value = {
        "id": session_id,
        "status": "active"
    }
    mock_count_chunks.return_value = 0

    response = client.post(f"/v1/sessions/{session_id}/complete")

    assert response.status_code == 400
    assert response.json()["detail"] == "upload at least one chunk before completing"
    mock_get_session.assert_called_once_with(session_id)
    mock_count_chunks.assert_called_once_with(session_id)


@patch("app.main.queue.enqueue_asr_job")
@patch("app.main.db.complete_session")
@patch("app.main.db.count_chunks")
@patch("app.main.db.get_session")
def test_complete_session_success(mock_get_session, mock_count_chunks, mock_complete_session, mock_enqueue_asr_job):
    session_id = uuid.uuid4()
    mock_get_session.return_value = {
        "id": session_id,
        "status": "active"
    }
    mock_count_chunks.return_value = 2
    mock_complete_session.return_value = {
        "id": session_id,
        "status": "completed",
        "school_id": "school_123"
    }

    response = client.post(f"/v1/sessions/{session_id}/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(session_id)
    assert data["status"] == "completed"
    assert data["chunks"] == 2
    assert data["job_enqueued"] == "asr"

    mock_get_session.assert_called_once_with(session_id)
    mock_count_chunks.assert_called_once_with(session_id)
    mock_complete_session.assert_called_once_with(session_id)
    mock_enqueue_asr_job.assert_called_once_with(session_id, "school_123")
