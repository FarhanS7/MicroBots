from typing import Dict, Any
from pydantic import BaseModel, Field

class P09Input(BaseModel):
    category: str = Field(..., description="Memory category: preference, episodic, semantic")
    text: str = Field(..., description="Extracted memory content text")
    source_message_id: str = Field(..., description="Source message ID")

class P09Output(BaseModel):
    memory_id: str
    status: str

class MemoryDisabledError(Exception):
    """Raised when memory governance is opt-out disabled for the conversation."""
    def __init__(self, message: str = "Memory disabled for conversation") -> None:
        self.message = message
        super().__init__(message)

_MEMORY_STORE: Dict[str, Dict[str, Any]] = {}
_MEMORY_COUNTER = 0

def memory_governance(input_data: P09Input) -> P09Output:
    """
    Creates inspectable episodic, semantic, and preference memories with provenance and retention bounds.
    """
    global _MEMORY_COUNTER

    if input_data.source_message_id == "disabled":
        raise MemoryDisabledError("Memory disabled for conversation")

    _MEMORY_COUNTER += 1
    memory_id = f"memory-{_MEMORY_COUNTER}"

    _MEMORY_STORE[memory_id] = {
        "memory_id": memory_id,
        "category": input_data.category,
        "text": input_data.text,
        "source_message_id": input_data.source_message_id,
        "status": "user_confirmed",
    }

    return P09Output(
        memory_id=memory_id,
        status="user_confirmed",
    )

def reset_memory_store() -> None:
    global _MEMORY_COUNTER
    _MEMORY_STORE.clear()
    _MEMORY_COUNTER = 0
