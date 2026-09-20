import pytest
from oap.connectors.mcp_client import (
    I02Input,
    MCPSchemaMismatchError,
    mcp_client,
)

def test_mcp_client_happy_path():
    inp = I02Input(
        server_id="mcp-1",
        tool="fixture.read",
        arguments={"id": "record-1"}
    )
    res = mcp_client(inp)
    assert res.result == {"name": "Fixture"}
    assert res.validated is True

def test_mcp_client_schema_mismatch():
    inp = I02Input(
        server_id="mcp-1",
        tool="invalid_schema_tool",
        arguments={"id": "record-1"}
    )
    with pytest.raises(MCPSchemaMismatchError):
        mcp_client(inp)
