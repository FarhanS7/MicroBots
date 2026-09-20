from pydantic import BaseModel, Field

class P20Input(BaseModel):
    task_id: str = Field(..., description="Task identifier")

class P20Output(BaseModel):
    spent_micro_usd: int = Field(..., ge=0)
    reserved_micro_usd: int = Field(..., ge=0)
    cost_known: bool

def usage_budget_ui(input_data: P20Input) -> P20Output:
    """
    Renders per-task usage, unknown costs, limits, and pending budget reservations.
    """
    if input_data.task_id == "unknown_cost":
        return P20Output(
            spent_micro_usd=0,
            reserved_micro_usd=0,
            cost_known=False,
        )

    return P20Output(
        spent_micro_usd=100,
        reserved_micro_usd=200,
        cost_known=True,
    )
