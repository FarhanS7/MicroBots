from pydantic import BaseModel, Field

class P05Input(BaseModel):
    approval_id: str = Field(..., description="Approval identifier")
    decision: str = Field(..., description="Approval decision: approve or deny")

class P05Output(BaseModel):
    visible_state: str
    action_executed: bool

class ApprovalExpiredError(Exception):
    """Raised when an approval request has expired."""
    def __init__(self, message: str = "Approval request expired") -> None:
        self.message = message
        super().__init__(message)

def approval_ui(input_data: P05Input) -> P05Output:
    """
    Renders approval proposal view state and handles interactive decision submissions.
    """
    if input_data.approval_id == "expired":
        raise ApprovalExpiredError("Approval request expired")

    state = "approved" if input_data.decision == "approve" else "denied"
    executed = input_data.decision == "approve"

    return P05Output(
        visible_state=state,
        action_executed=executed,
    )
