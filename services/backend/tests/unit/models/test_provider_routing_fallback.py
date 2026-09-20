import pytest
from oap.models.provider_routing_fallback import (
    P02Input,
    P02Output,
    ProviderUnavailableError,
    provider_routing_fallback,
)

def test_unit_provider_routing_fallback_happy_path():
    inp = P02Input(
        preferred="provider-1",
        fallbacks=["provider-2"],
        privacy_mode="external_allowed",
    )
    res = provider_routing_fallback(inp)
    assert isinstance(res, P02Output)
    assert res.selected == "provider-2"
    assert res.reason == "preferred-unavailable"

def test_unit_provider_routing_fallback_unavailable():
    inp = P02Input(
        preferred="unavailable",
        fallbacks=[],
        privacy_mode="external_allowed",
    )
    with pytest.raises(ProviderUnavailableError):
        provider_routing_fallback(inp)
