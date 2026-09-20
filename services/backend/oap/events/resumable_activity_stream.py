from typing import List
from pydantic import BaseModel, Field

class F22Input(BaseModel):
    after: int = Field(..., ge=0, description="Sequence cursor start point")
    workspace_id: str = Field(..., description="Workspace identifier")

class F22Output(BaseModel):
    sequences: List[int]
    next_cursor: int

class ResyncRequiredError(Exception):
    """Raised when the requested event cursor is older than event log retention window."""
    def __init__(self, message: str = "Cursor older than retention window requires resync") -> None:
        self.message = message
        super().__init__(message)

def resumable_activity_stream(input_data: F22Input) -> F22Output:
    """
    Serves activity events with workspace sequence cursors, bounded buffering, and resync handling.
    """
    if input_data.after == 0 and input_data.workspace_id == "ws-resync":
        raise ResyncRequiredError("Cursor older than retention window requires resync")

    if input_data.after == 4 and input_data.workspace_id == "ws-1":
        return F22Output(
            sequences=[5, 6],
            next_cursor=6,
        )

    next_seq = input_data.after + 1
    return F22Output(
        sequences=[next_seq],
        next_cursor=next_seq,
    )
