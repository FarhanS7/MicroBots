import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from oap.models.provider_capability_contract import (
    F12Input,
    F12Output,
    CapabilityUnsupportedError,
    provider_capability_contract,
)

def test_unit_provider_capability_contract_happy_path() -> None:
    inp = F12Input(provider_id="provider-1", required_capabilities=["tools"])
    out = provider_capability_contract(inp)
    assert out == F12Output(compatible=True, provider_id="provider-1")

def test_unit_provider_capability_contract_unsupported() -> None:
    inp = F12Input(provider_id="text-only-provider", required_capabilities=["tools"])
    with pytest.raises(CapabilityUnsupportedError):
        provider_capability_contract(inp)
