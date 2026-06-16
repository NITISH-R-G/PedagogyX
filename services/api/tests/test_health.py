from fastapi.testclient import TestClient
from app.main import app
from app.auth import verify_api_key

client = TestClient(app)
app.dependency_overrides[verify_api_key] = lambda: "mock"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "api"
    assert "version" in data
    assert "g2_prod_data" in data
