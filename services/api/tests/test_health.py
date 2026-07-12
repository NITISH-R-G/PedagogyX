
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "api"
    assert "version" in data
    assert "g2_prod_data" in data
