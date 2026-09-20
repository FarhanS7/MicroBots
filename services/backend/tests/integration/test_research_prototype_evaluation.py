import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_quality_evaluate_happy_path():
    payload = {"fixture_count": 10, "live_count": 5}
    response = client.post("/api/v1/quality/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["fixture_pass_required"] == 10
    assert data["live_pass_required"] == 4
    assert data["forbidden_actions_allowed"] == 0

def test_quality_evaluate_failure():
    payload = {"fixture_count": 0, "live_count": 0}
    response = client.post("/api/v1/quality/evaluate", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "EVALUATION_FAILED"
    assert "Fabricated citations detected in research evaluation" in data["error"]["message"]

def test_quality_evaluate_missing_field():
    response = client.post("/api/v1/quality/evaluate", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
