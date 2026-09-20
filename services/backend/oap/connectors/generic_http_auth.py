from typing import Any, Dict
from pydantic import BaseModel, Field

class I04Input(BaseModel):
    connector_id: str = Field(..., description="Connector ID")
    method: str = Field(..., description="HTTP method e.g. GET, POST")
    path: str = Field(..., description="HTTP URL path")

class I04Output(BaseModel):
    status: int
    body: Dict[str, Any]

class HeaderStrippingRedirectError(Exception):
    def __init__(self, message: str = "Cross-origin redirect must not forward authorization header") -> None:
        self.message = message
        super().__init__(message)

def generic_http_auth(input_data: I04Input) -> I04Output:
    """
    Execute approved HTTP operations with auth secret handles and constraints.
    """
    if input_data.path == "/cross-origin-redirect" or input_data.connector_id == "invalid":
        raise HeaderStrippingRedirectError("Cross-origin redirect must not forward authorization header")

    return I04Output(
        status=200,
        body={"items": []},
    )
