import pytest
from oap.plugins.plugin_event_ui_extension import (
    I09Input,
    PluginScopeViolationError,
    plugin_event_ui_extension,
)

def test_plugin_event_ui_extension_happy_path():
    inp = I09Input(
        plugin_id="plugin-1",
        event_type="task.completed"
    )
    res = plugin_event_ui_extension(inp)
    assert res.subscription_id == "plugin-subscription-1"
    assert res.scope == "ws-1"

def test_plugin_event_ui_extension_cross_workspace():
    inp = I09Input(
        plugin_id="plugin-1",
        event_type="unauthorized_cross_workspace"
    )
    with pytest.raises(PluginScopeViolationError):
        plugin_event_ui_extension(inp)
