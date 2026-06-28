import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
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


@patch("app.dat_routes.dat_db.get_dat_session")
def test_stop_dat_session_not_found(mock_get_dat_session):
    # Mock dat_db.get_dat_session to return None
    mock_get_dat_session.return_value = None

    # Generate a random UUID for the session
    session_id = uuid.uuid4()

    # Call the endpoint
    response = client.post(
        f"/v1/dat-sessions/{session_id}/stop",
        headers={"Authorization": "Bearer dev_api_key_placeholder"},
    )

    # Assert the response status code is 404
    assert response.status_code == 404

    # Assert the error message is correct
    assert response.json()["detail"] == "dat session not found"
