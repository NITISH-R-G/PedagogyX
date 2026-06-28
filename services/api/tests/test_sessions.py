from unittest.mock import patch
from fastapi.testclient import TestClient
import uuid

from app.main import app


class AuthedClient:
    def __init__(self, c):
        self.c = c

    def post(self, url, **kwargs):
        kwargs.setdefault("headers", {})["Authorization"] = "Bearer dev_api_key_placeholder"
        return self.c.post(url, **kwargs)

    def get(self, url, **kwargs):
        kwargs.setdefault("headers", {})["Authorization"] = "Bearer dev_api_key_placeholder"
        return self.c.get(url, **kwargs)


client = AuthedClient(TestClient(app))


@patch("app.main.db.insert_session")
def test_create_session(mock_insert_session):
    mock_id = uuid.uuid4()
    mock_insert_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz",
        "status": "active",
    }

    response = client.post(
        "/v1/sessions",
        json={"school_id": "school_123", "room_id": "room_abc", "teacher_id": "teacher_xyz"},
    )

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
        "status": "active",
    }

    response = client.post("/v1/sessions", json={"school_id": "school_123"})

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["status"] == "active"

    mock_insert_session.assert_called_once_with("school_123", None, None)


def test_create_session_missing_school_id():
    response = client.post(
        "/v1/sessions", json={"room_id": "room_abc", "teacher_id": "teacher_xyz"}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "school_id"]
    assert data["detail"][0]["type"] == "missing"


def test_create_session_empty_school_id():
    response = client.post(
        "/v1/sessions", json={"school_id": "", "room_id": "room_abc", "teacher_id": "teacher_xyz"}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "school_id"]
    assert data["detail"][0]["type"] == "string_too_short"


@patch("app.main.db.get_session")
@patch("app.main.storage.put_chunk")
@patch("app.main.db.insert_chunk")
def test_upload_chunk_success(mock_insert_chunk, mock_put_chunk, mock_get_session):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz",
        "status": "active",
    }
    mock_put_chunk.return_value = "s3_key_abc"
    mock_insert_chunk.return_value = {
        "chunk_index": 1,
        "object_key": "s3_key_abc",
        "size_bytes": 10,
    }

    response = client.post(
        f"/v1/sessions/{mock_id}/chunks/1",
        files={"file": ("test.txt", b"hello test", "text/plain")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == str(mock_id)
    assert data["chunk_index"] == 1
    assert data["object_key"] == "s3_key_abc"
    assert data["size_bytes"] == 10

    mock_get_session.assert_called_once_with(mock_id)
    mock_put_chunk.assert_called_once_with(mock_id, 1, b"hello test", "text/plain")
    mock_insert_chunk.assert_called_once_with(mock_id, 1, "s3_key_abc", 10, "text/plain")


def test_upload_chunk_invalid_index():
    mock_id = uuid.uuid4()
    response = client.post(
        f"/v1/sessions/{mock_id}/chunks/10000",
        files={"file": ("test.txt", b"hello test", "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid chunk_index"

    response = client.post(
        f"/v1/sessions/{mock_id}/chunks/-1",
        files={"file": ("test.txt", b"hello test", "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid chunk_index"


@patch("app.main.db.get_session")
def test_upload_chunk_session_not_found(mock_get_session):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = None

    response = client.post(
        f"/v1/sessions/{mock_id}/chunks/1",
        files={"file": ("test.txt", b"hello test", "text/plain")},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "session not found"


@patch("app.main.db.get_session")
def test_upload_chunk_invalid_status(mock_get_session):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz",
        "status": "completed",
    }

    response = client.post(
        f"/v1/sessions/{mock_id}/chunks/1",
        files={"file": ("test.txt", b"hello test", "text/plain")},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "session not accepting uploads"


@patch("app.main.db.get_session")
@patch("app.main.settings")
def test_upload_chunk_file_too_large(mock_settings, mock_get_session):
    mock_id = uuid.uuid4()
    mock_get_session.return_value = {
        "id": mock_id,
        "school_id": "school_123",
        "room_id": "room_abc",
        "teacher_id": "teacher_xyz",
        "status": "active",
    }
    mock_settings.max_upload_bytes = 5

    response = client.post(
        f"/v1/sessions/{mock_id}/chunks/1",
        files={"file": ("test.txt", b"hello test", "text/plain")},
    )
    assert response.status_code == 413
    assert response.json()["detail"] == "chunk exceeds max size"
