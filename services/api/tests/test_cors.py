from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_cors_preflight_headers():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization,Content-Type",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in [
        "http://localhost:3000",
        "*",
    ]
    assert "GET" in response.headers.get("access-control-allow-methods", "")


def test_cors_get_headers():
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in [
        "http://localhost:3000",
        "*",
    ]
