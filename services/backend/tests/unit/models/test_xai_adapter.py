import pytest
from oap.models.xai_adapter import (
    P18Input,
    P18Output,
    XaiRateLimitError,
    xai_adapter,
)

def test_xai_adapter_happy_path():
    inp = P18Input(provider="xai", required_capabilities=["tools"])
    out = xai_adapter(inp)
    assert out.conformance_passed is True
    assert out.provider == "xai"

def test_xai_adapter_error():
    inp = P18Input(provider="xai", required_capabilities=["rate_limit"])
    with pytest.raises(XaiRateLimitError) as exc_info:
        xai_adapter(inp)
    assert "xAI rate limit exceeded" in str(exc_info.value)
