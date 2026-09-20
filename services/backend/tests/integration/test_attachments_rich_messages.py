import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.conversation_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_attachments_rich_messages_api_happy_path():
    response = client.post(
        "/api/v1/conversation/attachments",
        json={"conversation_id": "conversation-1", "file_id": "file-1", "media_type": "image/png"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["attachment_id"] == "attachment-1"
    assert data["accepted"] is True

def test_attachments_rich_messages_api_missing_field():
    response = client.post(
        "/api/v1/conversation/attachments",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_attachments_rich_messages_api_invalid():
    response = client.post(
        "/api/v1/conversation/attachments",
        json={"conversation_id": "conversation-1", "file_id": "file-1", "media_type": "unsupported"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "Invalid or oversized attachment" in data["error"]["message"]
