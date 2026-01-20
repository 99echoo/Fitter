import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Fitter API"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_clothing_list():
    response = client.get("/api/clothing")
    assert response.status_code == 200
    assert "items" in response.json()
