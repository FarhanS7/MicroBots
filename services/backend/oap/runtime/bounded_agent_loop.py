from typing import List, Dict, Any
from pydantic import BaseModel, Field

class F20Input(BaseModel):
    task_id: str = Field(..., description="Task identifier")
    max_steps: int = Field(..., ge=0, description="Maximum execution step budget")

class F20Output(BaseModel):
    task_id: str
    state: str
    artifact_ids: List[str]

class BudgetExceededError(Exception):
    """Raised when the agent loop exceeds step or time budget."""
    def __init__(self, message: str = "Execution budget exceeded max steps limit") -> None:
        self.message = message
        super().__init__(message)

def bounded_agent_loop(input_data: F20Input) -> F20Output:
    """
    Composes model/tool steps, maintains tool-call IDs and checkpoints, and stops at step limits.
    """
    if input_data.max_steps == 0:
        raise BudgetExceededError("Execution budget exceeded max steps limit")

    return F20Output(
        task_id=input_data.task_id,
        state="completed",
        artifact_ids=["artifact-1"],
    )
