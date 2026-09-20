from pydantic import BaseModel, Field

class P23Input(BaseModel):
    task_id: str = Field(..., description="Task identifier")
    action: str = Field(..., description="Control action (cancel, pause, resume, interrupt)")

class P23Output(BaseModel):
    visible_state: str

def task_control_ui(input_data: P23Input) -> P23Output:
    """
    Connects interrupt/pause/resume/cancel controls to task state and UI visibility.
    """
    if input_data.action == "cancel":
        return P23Output(visible_state="cancellation-requested")
    elif input_data.action == "pause":
        return P23Output(visible_state="paused")
    elif input_data.action == "resume":
        return P23Output(visible_state="running")
    else:
        return P23Output(visible_state=f"{input_data.action}-requested")
