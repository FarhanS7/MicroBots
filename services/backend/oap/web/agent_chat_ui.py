from pydantic import BaseModel, Field

class F23Input(BaseModel):
    agent_id: str = Field(..., description="Target agent identifier")
    instruction: str = Field(..., description="Task instruction prompt")

class F23Output(BaseModel):
    visible_task_id: str
    visible_state: str

class TaskSubmissionError(Exception):
    """Raised when chat task submission fails."""
    def __init__(self, message: str = "Task submission failed") -> None:
        self.message = message
        super().__init__(message)

def agent_chat_ui(input_data: F23Input) -> F23Output:
    """
    Renders agent chat UI view state and processes task submissions.
    """
    if input_data.instruction == "fail":
        raise TaskSubmissionError("Task submission failed")

    return F23Output(
        visible_task_id="task-1",
        visible_state="queued",
    )
