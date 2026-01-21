def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Fitter API"


def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_clothing_list(test_client):
    response = test_client.get("/api/clothing")
    assert response.status_code == 200
    assert "items" in response.json()
