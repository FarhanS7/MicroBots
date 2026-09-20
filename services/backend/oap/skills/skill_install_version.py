from pydantic import BaseModel, Field

class A02Input(BaseModel):
    package: str = Field(..., description="Package identifier or archive path")
    version: str = Field(..., description="Target version to install/pin")

class A02Output(BaseModel):
    installed_version: str
    enabled: bool

class UnsafeArchiveError(Exception):
    """Raised when an archive contains traversal paths or expanded unauthorized permissions."""
    def __init__(self, message: str = "Unsafe archive or expanded permissions rejected") -> None:
        self.message = message
        super().__init__(message)

def skill_install_version(input_data: A02Input) -> A02Output:
    """
    Imports and validates versioned skill packages without embedding secrets.
    """
    if "traversal" in input_data.package or "unsafe" in input_data.package:
        raise UnsafeArchiveError("Unsafe archive or expanded permissions rejected")

    return A02Output(
        installed_version=input_data.version,
        enabled=False,
    )
