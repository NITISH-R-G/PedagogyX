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


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "api"
    assert "version" in data
    assert "g2_prod_data" in data
