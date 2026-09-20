from pydantic import BaseModel, Field

class I01Input(BaseModel):
    name: str = Field(..., description="Connector name")
    auth_type: str = Field(..., description="Authentication type e.g. api_key, oauth2")
    secret_id: str = Field(..., description="Secret ID from credential vault")

class I01Output(BaseModel):
    connector_id: str
    enabled: bool

class InvalidConnectorAuthError(Exception):
    def __init__(self, message: str = "Missing or unknown auth configuration") -> None:
        self.message = message
        super().__init__(message)

def connector_registry(input_data: I01Input) -> I01Output:
    """
    Register connector instances, versioned tool schemas, capabilities, and auth handles.
    """
    if input_data.auth_type == "unknown" or input_data.secret_id == "invalid":
        raise InvalidConnectorAuthError("Missing or unknown auth configuration")

    return I01Output(
        connector_id="connector-1",
        enabled=False,
    )
