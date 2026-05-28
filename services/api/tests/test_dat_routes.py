import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)





client.headers.update({"Authorization": "Bearer dev_api_key_placeholder"})



def test_stop_dat_session_error_path():
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
        "updated_at": None,
    }

    with patch("app.dat_routes.dat_db.get_dat_session") as mock_get_dat_session:
        mock_get_dat_session.return_value = mock_row

        with patch("app.dat_routes.dat_db.transition_stream_state") as mock_transition:
            mock_transition.side_effect = ValueError("Invalid transition")

            response = client.post(f"/v1/dat-sessions/{dat_session_id}/stop", headers={"Authorization": "Bearer dev_api_key_placeholder"})

            assert response.status_code == 400
            assert response.json() == {"detail": "Invalid transition"}


def test_stop_dat_session_not_found():
    dat_session_id = uuid.uuid4()

    with patch("app.dat_routes.dat_db.get_dat_session") as mock_get_dat_session:
        mock_get_dat_session.return_value = None

        response = client.post(f"/v1/dat-sessions/{dat_session_id}/stop", headers={"Authorization": "Bearer dev_api_key_placeholder"})

        assert response.status_code == 404
        assert response.json() == {"detail": "dat session not found"}
