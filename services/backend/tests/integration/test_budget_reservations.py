import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_usage_reserve_happy_path():
    payload = {"budget_micro_usd": 1000, "reserved_micro_usd": 200, "requested_micro_usd": 300}
    response = client.post("/api/v1/usage/reserve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is True
    assert data["reserved_micro_usd"] == 500

def test_usage_reserve_exceeded():
    payload = {"budget_micro_usd": 1000, "reserved_micro_usd": 900, "requested_micro_usd": 300}
    response = client.post("/api/v1/usage/reserve", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "BUDGET_EXCEEDED"

def test_usage_reserve_missing_field():
    response = client.post("/api/v1/usage/reserve", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
