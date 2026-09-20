import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.agents.agent_definition import reset_agents_store

client = TestClient(app)

def setup_function() -> None:
    reset_agents_store()

def test_agents_happy_path() -> None:
    response = client.post(
        "/api/v1/agents",
        json={
            "name": "Researcher",
            "role": "Research",
            "instruction": "Produce cited reports",
            "model_id": "model-1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "agent_id": "agent-1",
        "state": "idle",
        "revision": 1,
    }

def test_agents_missing_field() -> None:
    response = client.post("/api/v1/agents", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
