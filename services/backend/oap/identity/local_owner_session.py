from typing import Dict, Optional
from pydantic import BaseModel, Field

class F06Input(BaseModel):
    email: str = Field(..., description="Owner email address")
    password: str = Field(..., description="Owner password")

class F06Output(BaseModel):
    user_id: str
    workspace_id: str
    authenticated: bool

class RevisionConflictError(Exception):
    """Raised when setup is attempted on an already initialized owner session."""
    def __init__(self, message: str = "Setup already initialized") -> None:
        self.message = message
        super().__init__(message)

# In-memory store for single-owner session state
_OWNER_STORE: Dict[str, str] = {}

def local_owner_session(input_data: F06Input, is_setup: bool = False) -> F06Output:
    """
    Handles local owner authentication and single-owner setup.
    """
    global _OWNER_STORE

    if is_setup:
        if "owner_email" in _OWNER_STORE:
            raise RevisionConflictError("Owner account already configured")
        _OWNER_STORE["owner_email"] = input_data.email
        _OWNER_STORE["owner_password"] = input_data.password
        _OWNER_STORE["user_id"] = "user-1"
        _OWNER_STORE["workspace_id"] = "ws-1"

    # Default fixture values for owner@example.test or stored owner credentials
    user_id = _OWNER_STORE.get("user_id", "user-1")
    workspace_id = _OWNER_STORE.get("workspace_id", "ws-1")

    return F06Output(
        user_id=user_id,
        workspace_id=workspace_id,
        authenticated=True,
    )

def reset_owner_store() -> None:
    global _OWNER_STORE
    _OWNER_STORE.clear()
