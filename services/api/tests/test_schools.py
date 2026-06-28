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


@patch("app.main.db.school_overview")
def test_school_overview_success(mock_school_overview):
    mock_data = {
        "school_id": "test_school_1",
        "m_a_coverage": {
            "rooms_observed": 5,
            "rooms_target": 10,
            "coverage_pct": 50.0,
        },
        "m_b_median_insight_sec": 12.5,
        "sessions_total": 20,
        "sessions_completed": 15,
        "sessions_week": 5,
        "recent_sessions": [],
    }
    mock_school_overview.return_value = mock_data

    response = client.get("/v1/schools/test_school_1/overview")

    assert response.status_code == 200
    assert response.json() == mock_data
    mock_school_overview.assert_called_once_with("test_school_1")
