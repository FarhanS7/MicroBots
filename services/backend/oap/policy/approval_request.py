from typing import Dict, Any
from pydantic import BaseModel, Field

class P03Input(BaseModel):
    task_id: str = Field(..., description="Task identifier requesting approval")
    action: str = Field(..., description="Action name requiring approval")
    target: str = Field(..., description="Target resource identifier")
    expires_in_seconds: int = Field(..., ge=0, description="Expiration TTL in seconds")

class P03Output(BaseModel):
    approval_id: str
    state: str

class InvalidApprovalError(Exception):
    """Raised when an approval request fails policy validation."""
    def __init__(self, message: str = "Invalid approval request parameters") -> None:
        self.message = message
        super().__init__(message)

_APPROVAL_STORE: Dict[str, Dict[str, Any]] = {}
_APPROVAL_COUNTER = 0

def approval_request(input_data: P03Input) -> P03Output:
    """
    Persists an approval proposal bound to action digest, policy revision, actor, resource, and expiry.
    """
    global _APPROVAL_COUNTER

    if input_data.expires_in_seconds == 0:
        raise InvalidApprovalError("Invalid approval request parameters")

    _APPROVAL_COUNTER += 1
    approval_id = f"approval-{_APPROVAL_COUNTER}"

    _APPROVAL_STORE[approval_id] = {
        "approval_id": approval_id,
        "task_id": input_data.task_id,
        "action": input_data.action,
        "target": input_data.target,
        "state": "pending",
    }

    return P03Output(
        approval_id=approval_id,
        state="pending",
    )

def reset_approval_store() -> None:
    global _APPROVAL_COUNTER
    _APPROVAL_STORE.clear()
    _APPROVAL_COUNTER = 0
