import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.events.transactional_outbox import reset_outbox

client = TestClient(app)

def setup_function() -> None:
    reset_outbox()

def test_outbox_happy_path() -> None:
    response = client.post(
        "/api/v1/events/outbox",
        json={"aggregate_id": "task-1", "event_type": "task.created", "request_id": "request-1"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "event_id": "event-1",
        "sequence": 1,
    }

def test_outbox_deduplication() -> None:
    body = {"aggregate_id": "task-1", "event_type": "task.created", "request_id": "request-1"}
    r1 = client.post("/api/v1/events/outbox", json=body)
    r2 = client.post("/api/v1/events/outbox", json=body)
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json() == r2.json()

def test_outbox_missing_field() -> None:
    response = client.post("/api/v1/events/outbox", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
