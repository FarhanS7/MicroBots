import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_bootstrap_seed_happy_path():
    payload = {"environment": "test", "seed": "research-v1"}
    response = client.post("/api/v1/bootstrap/seed", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["seeded"] is True
    assert data["duplicate_rows"] == 0

def test_bootstrap_seed_production_refused():
    payload = {"environment": "production", "seed": "research-v1"}
    response = client.post("/api/v1/bootstrap/seed", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Production seeding refused" in data["error"]["message"]

def test_bootstrap_seed_missing_field():
    response = client.post("/api/v1/bootstrap/seed", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
