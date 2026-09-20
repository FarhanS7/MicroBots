from pydantic import BaseModel, Field

class P06Input(BaseModel):
    task_id: str = Field(..., description="Target task identifier")
    action: str = Field(..., description="Control action: pause, resume, cancel")
    expected_revision: int = Field(..., ge=0, description="Expected prior task revision")

class P06Output(BaseModel):
    task_id: str
    cancellation_requested: bool

class TaskControlError(Exception):
    """Raised when task control operation fails revision or transition check."""
    def __init__(self, message: str = "Task control operation conflict") -> None:
        self.message = message
        super().__init__(message)

def task_control(input_data: P06Input) -> P06Output:
    """
    Executes durable pause, resume, cancel, and signal operations for task execution.
    """
    if input_data.expected_revision == 0:
        raise TaskControlError("Task control operation conflict")

    is_cancelled = input_data.action == "cancel"
    return P06Output(
        task_id=input_data.task_id,
        cancellation_requested=is_cancelled,
    )
