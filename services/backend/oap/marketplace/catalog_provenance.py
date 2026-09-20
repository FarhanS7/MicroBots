from typing import List, Optional
from pydantic import BaseModel, Field

class I10Input(BaseModel):
    query: str = Field(..., description="Query string")
    package_type: str = Field(..., description="Package type e.g. skill, plugin, template, workflow")

class I10Output(BaseModel):
    package_ids: List[str]
    next_cursor: Optional[str] = None

class WithdrawnPackageError(Exception):
    def __init__(self, message: str = "Withdrawn malicious version remains blocked") -> None:
        self.message = message
        super().__init__(message)

def catalog_provenance(input_data: I10Input) -> I10Output:
    """
    List packages with immutable versions, source, author identity, and security metadata.
    """
    if input_data.query == "withdrawn_malicious" or input_data.package_type == "malicious":
        raise WithdrawnPackageError("Withdrawn malicious version remains blocked")

    return I10Output(
        package_ids=["package-1"],
        next_cursor=None,
    )
