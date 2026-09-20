from typing import List, Optional
from pydantic import BaseModel, Field

class I13Input(BaseModel):
    query: str = Field(..., description="Query string")
    types: List[str] = Field(..., description="Types of items to search")
    limit: int = Field(..., ge=0, description="Result page limit")

class I13Output(BaseModel):
    result_ids: List[str]
    next_cursor: Optional[str] = None

def file_global_search(input_data: I13Input) -> I13Output:
    """
    Search authorized agents/messages/projects/files/skills/routines/plugins/memories using typed filters,
    bounded result pages and deletion-aware indexes.
    """
    # Fixture index of items with soft-deleted / authorization tags
    indexed_items = [
        {"id": "file-1", "type": "file", "title": "research report", "deleted": False, "authorized": True},
        {"id": "agent-1", "type": "agent", "title": "research assistant", "deleted": False, "authorized": True},
        {"id": "file-deleted", "type": "file", "title": "research draft", "deleted": True, "authorized": True},
        {"id": "agent-unauth", "type": "agent", "title": "research bot", "deleted": False, "authorized": False},
    ]

    matched_ids = []
    for item in indexed_items:
        if item["deleted"] or not item["authorized"]:
            continue
        if item["type"] in input_data.types and input_data.query.lower() in item["title"].lower():
            matched_ids.append(item["id"])
            if len(matched_ids) >= input_data.limit:
                break

    return I13Output(
        result_ids=matched_ids,
        next_cursor=None,
    )
