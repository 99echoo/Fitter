import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_result_not_found():
    response = client.get("/api/result/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
