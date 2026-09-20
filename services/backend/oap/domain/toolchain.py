import os
from pydantic import BaseModel, Field, ValidationError

class F01Input(BaseModel):
    environment: str = Field(..., description="Target execution environment, e.g. local")

class F01Output(BaseModel):
    python_locked: bool
    javascript_locked: bool
    docs_check_available: bool

class ErrorDetail(BaseModel):
    code: str
    message: str
    retryable: bool = False

class PublicErrorEnvelope(BaseModel):
    error: ErrorDetail
    trace_id: str = "trace-test"

class PrerequisiteError(Exception):
    """Raised when mandatory toolchain dependencies or lockfiles are missing."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

def verify_toolchain_contract(input_data: F01Input, root_path: str | None = None) -> F01Output:
    """
    Executes F01 Toolchain Contract verification against repository configuration.
    Validates existence of Python lock/project configuration, JS/TS workspace configuration,
    and documentation check capability.
    """
    if root_path is None:
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

    pyproject_path = os.path.join(root_path, "services", "backend", "pyproject.toml")
    package_json_path = os.path.join(root_path, "package.json")
    docs_check_path = os.path.join(root_path, "scripts", "check_docs.py")

    python_locked = os.path.exists(pyproject_path)
    javascript_locked = os.path.exists(package_json_path)
    docs_check_available = os.path.exists(docs_check_path)

    if not (python_locked and javascript_locked):
        raise PrerequisiteError("Required toolchain runtime or lockfile is missing")

    return F01Output(
        python_locked=python_locked,
        javascript_locked=javascript_locked,
        docs_check_available=docs_check_available,
    )

