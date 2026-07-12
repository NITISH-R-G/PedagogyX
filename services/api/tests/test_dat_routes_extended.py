import uuid
from unittest.mock import patch
from datetime import datetime



def test_create_dat_session(client):
    mock_id = uuid.uuid4()
    mock_row = {
        "id": mock_id,
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
        "device_label": "device_1",
        "state": "IDLE",
        "stream_state": "STOPPED",
        "pedagogy_session_id": None,
        "updated_at": datetime.now(),
    }
    with patch("app.dat_routes.dat_db.create_dat_session") as mock_create, patch(
        "app.dat_routes.append_event"
    ) as mock_append:
        mock_create.return_value = mock_row

        response = client.post(
            "/v1/dat-sessions",
            json={
                "school_id": "school_1",
                "room_id": "room_1",
                "teacher_id": "teacher_1",
                "device_label": "device_1",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["dat_session_id"] == str(mock_id)
        assert data["state"] == "IDLE"
        mock_create.assert_called_once_with("school_1", "room_1", "teacher_1", "device_1")
        mock_append.assert_called_once()


def test_get_dat_session_not_found(client):
    dat_session_id = uuid.uuid4()
    with patch("app.dat_routes.dat_db.get_dat_session") as mock_get:
        mock_get.return_value = None

        response = client.get(f"/v1/dat-sessions/{dat_session_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "dat session not found"


def test_get_dat_session_success(client):
    dat_session_id = uuid.uuid4()
    mock_row = {
        "id": dat_session_id,
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
        "device_label": "device_1",
        "state": "STARTED",
        "stream_state": "STREAMING",
        "pedagogy_session_id": uuid.uuid4(),
        "updated_at": datetime.now(),
    }
    mock_events = [
        {
            "event_type": "SESSION_CREATED",
            "from_state": "IDLE",
            "to_state": "IDLE",
            "detail": {},
            "created_at": datetime.now(),
        }
    ]
    with patch("app.dat_routes.dat_db.get_dat_session") as mock_get, patch(
        "app.dat_routes.dat_db.list_events"
    ) as mock_list_events:
        mock_get.return_value = mock_row
        mock_list_events.return_value = mock_events

        response = client.get(f"/v1/dat-sessions/{dat_session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["dat_session_id"] == str(dat_session_id)
        assert len(data["recent_events"]) == 1
        assert data["recent_events"][0]["event_type"] == "SESSION_CREATED"


def test_post_lifecycle_session(client):
    dat_session_id = uuid.uuid4()
    mock_row = {
        "id": dat_session_id,
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
        "device_label": "device_1",
        "state": "STARTED",
        "stream_state": "STOPPED",
        "pedagogy_session_id": None,
        "updated_at": datetime.now(),
    }
    with patch("app.dat_routes.dat_db.transition_session_state") as mock_transition:
        mock_transition.return_value = mock_row

        response = client.post(
            f"/v1/dat-sessions/{dat_session_id}/lifecycle",
            json={
                "event_type": "session.started",
                "target": "session",
                "to_state": "STARTED",
            },
        )
        assert response.status_code == 200
        assert response.json()["state"] == "STARTED"


def test_post_lifecycle_stream_with_pedagogy_link(client):
    dat_session_id = uuid.uuid4()
    mock_row = {
        "id": dat_session_id,
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
        "device_label": "device_1",
        "state": "STARTED",
        "stream_state": "STREAMING",
        "pedagogy_session_id": None,
        "updated_at": datetime.now(),
    }
    pedagogy_id = uuid.uuid4()
    mock_pedagogy = {
        "id": pedagogy_id,
    }
    with patch("app.dat_routes.dat_db.transition_stream_state") as mock_transition, patch(
        "app.dat_routes.db.insert_session"
    ) as mock_insert_session, patch("app.dat_routes.dat_db.link_pedagogy_session"), patch(
        "app.dat_routes.append_event"
    ), patch(
        "app.dat_routes.dat_db.get_dat_session"
    ) as mock_get:
        mock_transition.return_value = mock_row
        mock_insert_session.return_value = mock_pedagogy
        mock_row_with_pedagogy = dict(mock_row, pedagogy_session_id=pedagogy_id)
        mock_get.return_value = mock_row_with_pedagogy

        response = client.post(
            f"/v1/dat-sessions/{dat_session_id}/lifecycle",
            json={
                "event_type": "stream.streaming",
                "target": "stream",
                "to_state": "STREAMING",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stream_state"] == "STREAMING"
        assert data["pedagogy_session_id"] == str(pedagogy_id)


def test_start_dat_session(client):
    dat_session_id = uuid.uuid4()
    mock_row = {
        "id": dat_session_id,
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
        "device_label": "device_1",
        "state": "STARTED",
        "stream_state": "STOPPED",
        "pedagogy_session_id": None,
        "updated_at": datetime.now(),
    }
    with patch("app.dat_routes.dat_db.transition_session_state") as mock_transition:
        mock_transition.side_effect = [None, mock_row]

        response = client.post(f"/v1/dat-sessions/{dat_session_id}/start")
        assert response.status_code == 200
        assert response.json()["state"] == "STARTED"


def test_start_stream(client):
    dat_session_id = uuid.uuid4()
    mock_row = {
        "id": dat_session_id,
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
        "device_label": "device_1",
        "state": "STARTED",
        "stream_state": "STREAMING",
        "pedagogy_session_id": uuid.uuid4(),
        "updated_at": datetime.now(),
    }
    with patch("app.dat_routes.dat_db.get_dat_session") as mock_get, patch(
        "app.dat_routes.dat_db.transition_stream_state"
    ) as mock_transition:
        mock_get.return_value = mock_row
        mock_transition.side_effect = [None, mock_row]

        response = client.post(f"/v1/dat-sessions/{dat_session_id}/stream/start")
        assert response.status_code == 200
        assert response.json()["stream_state"] == "STREAMING"
