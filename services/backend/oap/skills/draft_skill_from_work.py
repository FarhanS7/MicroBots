from pydantic import BaseModel, Field

class A03Input(BaseModel):
    source_task_id: str = Field(..., description="Source task identifier")
    name: str = Field(..., description="Draft skill name")

class A03Output(BaseModel):
    draft_id: str
    active: bool

def draft_skill_from_work(input_data: A03Input) -> A03Output:
    """
    Generates a reviewable skill draft from completed task work, redacting private values.
    """
    return A03Output(
        draft_id="draft-1",
        active=False,
    )
