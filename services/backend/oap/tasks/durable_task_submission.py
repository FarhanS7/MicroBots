from typing import Dict, Any
from pydantic import BaseModel, Field

class F14Input(BaseModel):
    agent_id: str = Field(..., description="Target agent ID")
    instruction: str = Field(..., description="Task instruction prompt")
    idempotency_key: str = Field(..., description="Stable request idempotency key")

class F14Output(BaseModel):
    task_id: str
    state: str
    revision: int = Field(..., ge=0)

class TaskIdempotencyConflictError(Exception):
    """Raised when an idempotency key is reused with a different instruction."""
    def __init__(self, message: str = "Idempotency key reused with different instruction") -> None:
        self.message = message
        super().__init__(message)

_TASKS_STORE: Dict[str, Dict[str, Any]] = {}
_TASK_COUNTER: int = 0

def durable_task_submission(input_data: F14Input) -> F14Output:
    """
    Submits a task durably into queued state with idempotency validation.
    """
    global _TASK_COUNTER

    if input_data.idempotency_key in _TASKS_STORE:
        existing = _TASKS_STORE[input_data.idempotency_key]
        if existing["instruction"] != input_data.instruction:
            raise TaskIdempotencyConflictError("Idempotency key reused with different instruction")
        return F14Output(
            task_id=str(existing["task_id"]),
            state=str(existing["state"]),
            revision=int(existing["revision"]),
        )

    _TASK_COUNTER += 1
    task_id = f"task-{_TASK_COUNTER}"
    state = "queued"
    revision = 1

    record = {
        "task_id": task_id,
        "agent_id": input_data.agent_id,
        "instruction": input_data.instruction,
        "idempotency_key": input_data.idempotency_key,
        "state": state,
        "revision": revision,
    }

    _TASKS_STORE[input_data.idempotency_key] = record

    return F14Output(
        task_id=task_id,
        state=state,
        revision=revision,
    )

def reset_tasks_store() -> None:
    global _TASK_COUNTER
    _TASKS_STORE.clear()
    _TASK_COUNTER = 0
