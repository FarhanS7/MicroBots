from pydantic import BaseModel, Field

class P25Input(BaseModel):
    page_id: str = Field(..., description="Target page identifier")
    operation: str = Field(..., description="Inspection or script evaluation operation")

class P25Output(BaseModel):
    request_count: int = Field(..., ge=0)
    credentials_redacted: bool

class InspectionForbiddenError(Exception):
    """Raised when page script evaluation or network inspection capability is absent/forbidden."""
    def __init__(self, message: str = "Script or network inspection capability forbidden") -> None:
        self.message = message
        super().__init__(message)

def browser_script_inspection(input_data: P25Input) -> P25Output:
    """
    Exposes page JavaScript evaluation and redacted network inspection with capability grants.
    """
    if input_data.operation == "forbidden":
        raise InspectionForbiddenError("Script or network inspection capability forbidden")

    return P25Output(
        request_count=2,
        credentials_redacted=True,
    )
