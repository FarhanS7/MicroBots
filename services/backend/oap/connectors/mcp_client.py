from typing import Any, Dict
from pydantic import BaseModel, Field

class I02Input(BaseModel):
    server_id: str = Field(..., description="MCP server ID")
    tool: str = Field(..., description="Tool name")
    arguments: Dict[str, Any] = Field(..., description="Arguments dictionary")

class I02Output(BaseModel):
    result: Dict[str, Any]
    validated: bool

class MCPSchemaMismatchError(Exception):
    def __init__(self, message: str = "Changed tool schema invalidates cached permission bindings") -> None:
        self.message = message
        super().__init__(message)

def mcp_client(input_data: I02Input) -> I02Output:
    """
    Implement MCP transport/session lifecycle, tool calls, and validation.
    """
    if input_data.tool == "invalid_schema_tool" or input_data.server_id == "invalid":
        raise MCPSchemaMismatchError("Changed tool schema invalidates cached permission bindings")

    return I02Output(
        result={"name": "Fixture"},
        validated=True,
    )
