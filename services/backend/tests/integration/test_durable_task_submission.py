import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.tasks.durable_task_submission import reset_tasks_store

client = TestClient(app)

def setup_function() -> None:
    reset_tasks_store()

def test_tasks_happy_path() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "agent_id": "agent-1",
            "instruction": "Research three competitors",
            "idempotency_key": "request-1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "task_id": "task-1",
        "state": "queued",
        "revision": 1,
    }

def test_tasks_idempotency_conflict() -> None:
    client.post(
        "/api/v1/tasks",
        json={"agent_id": "agent-1", "instruction": "Instruction A", "idempotency_key": "request-1"},
    )
    response = client.post(
        "/api/v1/tasks",
        json={"agent_id": "agent-1", "instruction": "Instruction B", "idempotency_key": "request-1"},
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "IDEMPOTENCY_CONFLICT",
            "message": "Idempotency key reused with different instruction",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }

def test_tasks_missing_field() -> None:
    response = client.post("/api/v1/tasks", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
