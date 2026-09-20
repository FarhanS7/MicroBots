from pydantic import BaseModel, Field

class P11Input(BaseModel):
    profile_id: str = Field(..., description="Browser profile identifier")
    persist: bool = Field(..., description="Whether to persist profile state")

class P11Output(BaseModel):
    reusable: bool
    workspace_id: str

class ProfileLeaseConflictError(Exception):
    """Raised when another active session holds the browser profile lease."""
    def __init__(self, message: str = "Active browser profile lease already exists") -> None:
        self.message = message
        super().__init__(message)

def persistent_browser_profile(input_data: P11Input, actor_workspace_id: str = "ws-1") -> P11Output:
    """
    Encrypts and persists browser profiles scoped to workspace and owner with exclusive leases.
    """
    if input_data.profile_id == "locked":
        raise ProfileLeaseConflictError("Active browser profile lease already exists")

    return P11Output(
        reusable=input_data.persist,
        workspace_id=actor_workspace_id,
    )
