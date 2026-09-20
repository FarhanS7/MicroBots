import pytest
from oap.web.model_settings_ui import (
    P19Input,
    P19Output,
    ConnectionFailedError,
    model_settings_ui,
)

def test_model_settings_ui_happy_path():
    inp = P19Input(provider_id="local-1", privacy_mode="local_only")
    out = model_settings_ui(inp)
    assert out.saved is True
    assert out.locality_indicator == "local"

def test_model_settings_ui_connection_error():
    inp = P19Input(provider_id="unreachable", privacy_mode="cloud_allowed")
    with pytest.raises(ConnectionFailedError) as exc_info:
        model_settings_ui(inp)
    assert "Provider endpoint connectivity failed" in str(exc_info.value)
