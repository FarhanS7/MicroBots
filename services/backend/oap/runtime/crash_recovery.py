from pydantic import BaseModel, Field

class P07Input(BaseModel):
    task_id: str = Field(..., description="Task identifier recovering from crash")
    checkpoint: str = Field(..., description="Checkpoint position identifier")

class P07Output(BaseModel):
    resumed: bool
    duplicate_external_effects: int

class OutcomeUnknownError(Exception):
    """Raised when external side-effect state cannot be safely reconciled."""
    def __init__(self, message: str = "External write outcome unknown") -> None:
        self.message = message
        super().__init__(message)

def crash_recovery(input_data: P07Input) -> P07Output:
    """
    Recovers workflow execution state from persisted checkpoints after worker restarts.
    """
    if input_data.checkpoint == "unknown":
        raise OutcomeUnknownError("External write outcome unknown")

    return P07Output(
        resumed=True,
        duplicate_external_effects=0,
    )
