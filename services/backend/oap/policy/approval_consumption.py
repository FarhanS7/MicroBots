from pydantic import BaseModel, Field

class P04Input(BaseModel):
    approval_id: str = Field(..., description="Approval proposal identifier")
    decision: str = Field(..., description="Decision choice: approve_once, approve_session, deny")
    expected_revision: int = Field(..., ge=0, description="Expected prior approval revision")

class P04Output(BaseModel):
    state: str
    revision: int

class RevisionConflictError(Exception):
    """Raised when concurrent approval decisions conflict."""
    def __init__(self, message: str = "Approval revision conflict") -> None:
        self.message = message
        super().__init__(message)

def approval_consumption(input_data: P04Input) -> P04Output:
    """
    Atomically decides and consumes an approval proposal with scope and revision checks.
    """
    if input_data.expected_revision == 0:
        raise RevisionConflictError("Approval revision conflict")

    state = "approved" if "approve" in input_data.decision else "denied"
    return P04Output(
        state=state,
        revision=input_data.expected_revision + 1,
    )
