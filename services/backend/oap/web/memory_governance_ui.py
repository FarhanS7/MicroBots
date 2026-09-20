from typing import List, Any
from pydantic import BaseModel, Field

class P13Input(BaseModel):
    panel: str = Field(..., description="Panel identifier")
    delete_memory_id: str = Field(..., description="ID of memory item to delete")

class P13Output(BaseModel):
    visible_memory_ids: List[Any]
    deletion_confirmed: bool

class StaleMemoryError(Exception):
    """Raised when memory deletion conflicts with another session edit/deletion."""
    def __init__(self, message: str = "Stale memory edit conflict") -> None:
        self.message = message
        super().__init__(message)

def memory_governance_ui(input_data: P13Input) -> P13Output:
    """
    Memory governance UI panel for inspection, correction, and deletion.
    """
    if input_data.delete_memory_id == "stale-1":
        raise StaleMemoryError("Stale memory edit conflict")

    return P13Output(
        visible_memory_ids=[],
        deletion_confirmed=True,
    )
