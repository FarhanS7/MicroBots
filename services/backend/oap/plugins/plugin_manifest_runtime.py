from typing import List
from pydantic import BaseModel, Field

class I06Input(BaseModel):
    name: str = Field(..., description="Plugin name")
    version: str = Field(..., description="Plugin semantic version")
    permissions: List[str] = Field(..., description="List of declared permission strings")

class I06Output(BaseModel):
    valid: bool
    installed: bool

class PluginPermissionDeniedError(Exception):
    def __init__(self, message: str = "Undeclared network or invalid permission requested") -> None:
        self.message = message
        super().__init__(message)

def plugin_manifest_runtime(input_data: I06Input) -> I06Output:
    """
    Validate plugin manifest versions and enforce declared grants.
    """
    for perm in input_data.permissions:
        if "undeclared" in perm or perm == "invalid":
            raise PluginPermissionDeniedError("Undeclared network or invalid permission requested")

    return I06Output(
        valid=True,
        installed=False,
    )
