from typing import Dict, Any
from pydantic import BaseModel, Field

class F16Input(BaseModel):
    task_id: str = Field(..., description="Task identifier")
    workspace_id: str = Field(..., description="Workspace identifier")
    image: str = Field(..., description="Docker image tag")

class F16Output(BaseModel):
    computer_id: str
    state: str

class ForbiddenGrantError(Exception):
    """Raised when an actor attempts to provision a sandbox with an invalid or expired workspace grant."""
    def __init__(self, message: str = "Invalid or expired workspace grant") -> None:
        self.message = message
        super().__init__(message)

_COMPUTERS_STORE: Dict[str, Dict[str, Any]] = {}
_COMPUTER_COUNTER: int = 0

def sandbox_broker(input_data: F16Input, actor_workspace_id: str = "ws-1") -> F16Output:
    """
    Provisions an ephemeral sandboxed execution container.
    """
    global _COMPUTER_COUNTER

    if actor_workspace_id != input_data.workspace_id:
        raise ForbiddenGrantError("Invalid or expired workspace grant")

    _COMPUTER_COUNTER += 1
    computer_id = f"computer-{_COMPUTER_COUNTER}"
    state = "ready"

    _COMPUTERS_STORE[computer_id] = {
        "computer_id": computer_id,
        "task_id": input_data.task_id,
        "workspace_id": input_data.workspace_id,
        "image": input_data.image,
        "state": state,
    }

    return F16Output(
        computer_id=computer_id,
        state=state,
    )

def reset_computers_store() -> None:
    global _COMPUTER_COUNTER
    _COMPUTERS_STORE.clear()
    _COMPUTER_COUNTER = 0
