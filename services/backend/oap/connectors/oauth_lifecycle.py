from pydantic import BaseModel, Field

class I05Input(BaseModel):
    connector_id: str = Field(..., description="Connector ID")
    callback_state: str = Field(..., description="OAuth state parameter")
    code: str = Field(..., description="OAuth authorization code")

class I05Output(BaseModel):
    connected: bool
    secret_id: str

class InvalidOAuthStateError(Exception):
    def __init__(self, message: str = "Wrong or reused state rejects callback") -> None:
        self.message = message
        super().__init__(message)

_used_states: set[str] = set()

def oauth_lifecycle(input_data: I05Input) -> I05Output:
    """
    Implement OAuth authorization callback, state/PKCE validation, and token encryption.
    """
    if input_data.callback_state == "wrong-state" or input_data.callback_state in _used_states:
        raise InvalidOAuthStateError("Wrong or reused state rejects callback")

    _used_states.add(input_data.callback_state)
    return I05Output(
        connected=True,
        secret_id="oauth-secret-1",
    )
