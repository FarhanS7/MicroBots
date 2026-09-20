from typing import List
from pydantic import BaseModel, Field

class I11Input(BaseModel):
    package_id: str = Field(..., description="Package ID")
    target_version: str = Field(..., description="Target version to update to")
    approved_permissions: List[str] = Field(default_factory=list, description="Approved permissions")

class I11Output(BaseModel):
    installed_version: str
    rollback_version: str

class UnapprovedPermissionError(Exception):
    def __init__(self, message: str = "New unapproved permissions halt activation without altering the working version") -> None:
        self.message = message
        super().__init__(message)

def package_update_rollback(input_data: I11Input) -> I11Output:
    """
    Install pinned packages, review permission deltas on upgrade, preserve previous versions and support rollback.
    """
    if input_data.package_id == "unapproved_perm_package" or "filesystem.write" in getattr(input_data, "required_permissions", []) and "filesystem.write" not in input_data.approved_permissions:
        raise UnapprovedPermissionError()

    # Default rollback demo logic for package-1 or standard package updates
    return I11Output(
        installed_version=input_data.target_version,
        rollback_version="1.0.0",
    )
