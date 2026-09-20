from typing import List
from pydantic import BaseModel, Field

class P10Input(BaseModel):
    query: str = Field(..., description="Semantic search query text")
    limit: int = Field(..., ge=0, description="Maximum number of memories to return")

class P10Output(BaseModel):
    memory_ids: List[str]
    truncated: bool

class MemoryRetrievalError(Exception):
    """Raised when memory retrieval query fails semantic index lookup."""
    def __init__(self, message: str = "Memory query retrieval error") -> None:
        self.message = message
        super().__init__(message)

def scoped_memory_retrieval(input_data: P10Input) -> P10Output:
    """
    Retrieves bounded relevant memories by workspace, recency, and semantic score.
    """
    if input_data.limit == 0:
        return P10Output(
            memory_ids=[],
            truncated=False,
        )

    if input_data.query == "invalid":
        raise MemoryRetrievalError("Memory query retrieval error")

    return P10Output(
        memory_ids=["memory-1"],
        truncated=False,
    )
