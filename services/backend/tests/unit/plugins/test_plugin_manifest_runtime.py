import pytest
from oap.plugins.plugin_manifest_runtime import (
    I06Input,
    PluginPermissionDeniedError,
    plugin_manifest_runtime,
)

def test_plugin_manifest_runtime_happy_path():
    inp = I06Input(
        name="fixture-plugin",
        version="1.0.0",
        permissions=["network:fixture.example.test"]
    )
    res = plugin_manifest_runtime(inp)
    assert res.valid is True
    assert res.installed is False

def test_plugin_manifest_runtime_permission_denied():
    inp = I06Input(
        name="fixture-plugin",
        version="1.0.0",
        permissions=["undeclared_network"]
    )
    with pytest.raises(PluginPermissionDeniedError):
        plugin_manifest_runtime(inp)
