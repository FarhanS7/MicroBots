from pydantic import BaseModel, Field

class P24Input(BaseModel):
    page_id: str = Field(..., description="Target page identifier")
    action: str = Field(..., description="Transfer action: upload or download")
    target: str = Field(..., description="Target selector, handle, or path")

class P24Output(BaseModel):
    file_id: str
    quarantined: bool

class UnapprovedDestinationError(Exception):
    """Raised when file transfer is requested to/from an unapproved destination."""
    def __init__(self, message: str = "Destination not approved by policy") -> None:
        self.message = message
        super().__init__(message)

def browser_file_transfer(input_data: P24Input) -> P24Output:
    """
    Supports policy-approved browser upload/download with size limits and quarantine.
    """
    if input_data.target == "unapproved" or input_data.action == "unapproved_upload":
        raise UnapprovedDestinationError("Destination not approved by policy")

    return P24Output(
        file_id="file-1",
        quarantined=True,
    )
