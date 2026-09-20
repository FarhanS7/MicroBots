import pytest
from oap.connectors.connector_registry import (
    I01Input,
    InvalidConnectorAuthError,
    connector_registry,
)

def test_connector_registry_happy_path():
    inp = I01Input(
        name="fixture-crm",
        auth_type="api_key",
        secret_id="secret-1"
    )
    res = connector_registry(inp)
    assert res.connector_id == "connector-1"
    assert res.enabled is False

def test_connector_registry_invalid_auth():
    inp = I01Input(
        name="fixture-crm",
        auth_type="unknown",
        secret_id="secret-1"
    )
    with pytest.raises(InvalidConnectorAuthError):
        connector_registry(inp)
