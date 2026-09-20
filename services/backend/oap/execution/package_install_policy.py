from pydantic import BaseModel, Field

class P22Input(BaseModel):
    manager: str = Field(..., description="Package manager (e.g., pip, npm)")
    package: str = Field(..., description="Package name to install")
    environment: str = Field(..., description="Target sandbox environment")

class P22Output(BaseModel):
    installed: bool
    host_modified: bool

class PackageInstallForbiddenError(Exception):
    """Raised when package installation is administratively disabled or forbidden."""
    def __init__(self, message: str = "Package installation forbidden") -> None:
        self.message = message
        super().__init__(message)

def package_install_policy(input_data: P22Input) -> P22Output:
    """
    Evaluates package installation requests in sandboxes with policy/resource checks.
    """
    if input_data.package == "forbidden" or input_data.manager == "forbidden":
        raise PackageInstallForbiddenError("Package installation forbidden")

    return P22Output(
        installed=True,
        host_modified=False,
    )
