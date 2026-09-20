import pytest
from oap.web.private_mode_indicator import (
    P30Input,
    P30Output,
    IncompatibleProviderError,
    private_mode_indicator,
)

def test_private_mode_indicator_happy_path():
    inp = P30Input(privacy_mode="local_only", provider_id="local-1")
    out = private_mode_indicator(inp)
    assert out.external_model_contact is False
    assert out.indicator == "local-only"

def test_private_mode_indicator_incompatible():
    inp = P30Input(privacy_mode="local_only", provider_id="openai-cloud")
    with pytest.raises(IncompatibleProviderError) as exc_info:
        private_mode_indicator(inp)
    assert "Incompatible remote provider under local-only mode" in str(exc_info.value)
