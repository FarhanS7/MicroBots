from pydantic import BaseModel, Field

class P08Input(BaseModel):
    budget_micro_usd: int = Field(..., ge=0, description="Total micro USD budget limit")
    reserved_micro_usd: int = Field(..., ge=0, description="Currently reserved micro USD amount")
    requested_micro_usd: int = Field(..., ge=0, description="Requested micro USD reservation amount")

class P08Output(BaseModel):
    allowed: bool
    reserved_micro_usd: int

class BudgetExceededError(Exception):
    """Raised when budget reservation limit is exceeded."""
    def __init__(self, message: str = "Budget reservation limit exceeded") -> None:
        self.message = message
        super().__init__(message)

def budget_reservations(input_data: P08Input) -> P08Output:
    """
    Reserves tokens/cost budgets before task dispatch and settles actual usage against limits.
    """
    new_reserved = input_data.reserved_micro_usd + input_data.requested_micro_usd

    if new_reserved > input_data.budget_micro_usd:
        raise BudgetExceededError("Budget reservation limit exceeded")

    return P08Output(
        allowed=True,
        reserved_micro_usd=new_reserved,
    )
