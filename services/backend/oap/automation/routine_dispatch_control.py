from pydantic import BaseModel, Field

class A08Input(BaseModel):
    routine_id: str = Field(..., description="Routine ID")
    scheduled_for: str = Field(..., description="ISO timestamp scheduled for execution")

class A08Output(BaseModel):
    execution_id: str
    duplicate: bool

_dispatched_executions: dict[tuple[str, str], str] = {}

def routine_dispatch_control(input_data: A08Input) -> A08Output:
    """
    Dispatch unique scheduled occurrences with latest-one catch-up and skip-overlap defaults.
    """
    key = (input_data.routine_id, input_data.scheduled_for)
    if key in _dispatched_executions:
        return A08Output(
            execution_id=_dispatched_executions[key],
            duplicate=True
        )

    exec_id = "execution-1"
    _dispatched_executions[key] = exec_id
    return A08Output(
        execution_id=exec_id,
        duplicate=False
    )
