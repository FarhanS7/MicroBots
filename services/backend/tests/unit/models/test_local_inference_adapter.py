import pytest
from oap.models.local_inference_adapter import (
    P01Input,
    P01Output,
    LocalModelUnavailableError,
    local_inference_adapter,
)

def test_unit_local_inference_adapter_happy_path():
    inp = P01Input(endpoint="http://local-model:11434", privacy_mode="local_only")
    res = local_inference_adapter(inp)
    assert isinstance(res, P01Output)
    assert res.provider_id == "local-1"
    assert res.external_requests == 0

def test_unit_local_inference_adapter_unavailable():
    inp = P01Input(endpoint="http://unreachable:11434", privacy_mode="local_only")
    with pytest.raises(LocalModelUnavailableError):
        local_inference_adapter(inp)
