import pytest
from oap.models.anthropic_adapter import (
    P16Input,
    P16Output,
    AdapterConformanceError,
    anthropic_adapter,
)

def test_anthropic_adapter_happy_path():
    inp = P16Input(provider="anthropic", required_capabilities=["tools"])
    out = anthropic_adapter(inp)
    assert out.conformance_passed is True
    assert out.provider == "anthropic"

def test_anthropic_adapter_error():
    inp = P16Input(provider="anthropic", required_capabilities=["unsupported"])
    with pytest.raises(AdapterConformanceError) as exc_info:
        anthropic_adapter(inp)
    assert "Anthropic adapter conformance failed" in str(exc_info.value)
