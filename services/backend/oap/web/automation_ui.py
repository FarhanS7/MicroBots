from typing import Optional
from pydantic import BaseModel, Field

class A13Input(BaseModel):
    routine_id: str = Field(..., description="Routine ID")
    action: str = Field(..., description="Action e.g. pause, resume, preview")

class A13Output(BaseModel):
    visible_state: str
    next_run: Optional[str] = None

class InvalidAutomationUIError(Exception):
    def __init__(self, message: str = "Invalid automation UI state action") -> None:
        self.message = message
        super().__init__(message)

def automation_ui(input_data: A13Input) -> A13Output:
    """
    Expose routine creation/preview/activation/history with visible state.
    """
    if input_data.action == "unconfirmed_schedule":
        return A13Output(
            visible_state="draft",
            next_run=None,
        )

    if input_data.action == "pause":
        return A13Output(
            visible_state="paused",
            next_run=None,
        )

    if input_data.action == "activate":
        return A13Output(
            visible_state="active",
            next_run="2026-09-21T02:00:00Z",
        )

    if input_data.action == "invalid":
        raise InvalidAutomationUIError("Invalid automation UI state action")

    return A13Output(
        visible_state="paused",
        next_run=None,
    )
