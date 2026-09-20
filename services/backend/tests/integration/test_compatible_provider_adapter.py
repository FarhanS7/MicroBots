import sys
import os
from unittest.mock import patch
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.models.compatible_provider_adapter import StreamTruncatedError

client = TestClient(app)

def test_generate_happy_path() -> None:
    response = client.post(
        "/api/v1/models/generate",
        json={"model_id": "model-1", "prompt": "Say hello", "max_output_tokens": 20},
    )
    assert response.status_code == 200
    assert response.json() == {
        "text": "Hello",
        "input_tokens": 4,
        "output_tokens": 1,
    }

def test_generate_stream_truncated() -> None:
    with patch("oap.api.models_router.compatible_provider_adapter", side_effect=StreamTruncatedError("Stream truncated before completion")):
        response = client.post(
            "/api/v1/models/generate",
            json={"model_id": "model-1", "prompt": "Say hello", "max_output_tokens": 20},
        )
        assert response.status_code == 422
        assert response.json() == {
            "error": {
                "code": "STREAM_TRUNCATED_ERROR",
                "message": "Stream truncated before completion",
                "retryable": False,
            },
            "trace_id": "trace-test",
        }

def test_generate_missing_field() -> None:
    response = client.post("/api/v1/models/generate", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
