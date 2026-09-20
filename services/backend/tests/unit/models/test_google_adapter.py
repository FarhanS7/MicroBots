import pytest
from oap.models.google_adapter import (
    P17Input,
    P17Output,
    GoogleCapabilityUnsupportedError,
    google_adapter,
)

def test_google_adapter_happy_path():
    inp = P17Input(provider="google", required_capabilities=["tools"])
    out = google_adapter(inp)
    assert out.conformance_passed is True
    assert out.provider == "google"

def test_google_adapter_error():
    inp = P17Input(provider="google", required_capabilities=["multimodal"])
    with pytest.raises(GoogleCapabilityUnsupportedError) as exc_info:
        google_adapter(inp)
    assert "Google capability unsupported" in str(exc_info.value)
