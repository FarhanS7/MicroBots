from pydantic import BaseModel, Field

class A15Input(BaseModel):
    file_id: str = Field(..., description="File ID")
    revision: int = Field(..., ge=0, description="File revision number")

class A15Output(BaseModel):
    event_type: str
    delivery_count: int

_file_cursors: dict[str, int] = {}

def file_watch_trigger(input_data: A15Input) -> A15Output:
    """
    Translate workspace file changes into deduplicated events using file revisions.
    """
    last_rev = _file_cursors.get(input_data.file_id, 0)
    if input_data.revision <= last_rev:
        return A15Output(
            event_type="file.unchanged",
            delivery_count=0
        )

    _file_cursors[input_data.file_id] = input_data.revision
    return A15Output(
        event_type="file.created",
        delivery_count=1
    )
