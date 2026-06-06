from unittest.mock import patch
from fastapi.testclient import TestClient
import uuid

from app.main import app

client = TestClient(app)
client.headers.update({"Authorization": "Bearer dev_api_key_placeholder"})


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
