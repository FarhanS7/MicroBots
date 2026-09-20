import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.conversation.persistent_messages import reset_conversation_store

client = TestClient(app)

def setup_function() -> None:
    reset_conversation_store()

def test_messages_happy_path() -> None:
    response = client.post(
        "/api/v1/conversation/messages",
        json={
            "agent_id": "agent-1",
            "client_message_id": "msg-client-1",
            "text": "Research three competitors",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "conversation_id": "conversation-1",
        "message_id": "message-1",
        "sequence": 1,
    }

def test_messages_idempotency_conflict() -> None:
    client.post(
        "/api/v1/conversation/messages",
        json={"agent_id": "agent-1", "client_message_id": "msg-client-1", "text": "Text A"},
    )
    response = client.post(
        "/api/v1/conversation/messages",
        json={"agent_id": "agent-1", "client_message_id": "msg-client-1", "text": "Text B"},
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "IDEMPOTENCY_CONFLICT",
            "message": "Client message ID reused with different content",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }

def test_messages_missing_field() -> None:
    response = client.post("/api/v1/conversation/messages", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
