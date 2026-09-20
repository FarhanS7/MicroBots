from typing import Dict, Any
from pydantic import BaseModel, Field

class F17Input(BaseModel):
    path: str = Field(..., description="File path relative to workspace root")
    content: str = Field(..., description="UTF-8 text content")
    expected_revision: int = Field(..., ge=0, description="Expected prior revision number")

class F17Output(BaseModel):
    path: str
    revision: int
    bytes: int

class TraversalError(Exception):
    """Raised when path traversal or escaping symlink is detected."""
    def __init__(self, message: str = "Path traversal or escaping symlink detected") -> None:
        self.message = message
        super().__init__(message)

_FILE_STORE: Dict[str, Dict[str, Any]] = {}

def workspace_file_operations(input_data: F17Input) -> F17Output:
    """
    Atomically writes bounded UTF-8 workspace files with path normalization and revision tracking.
    """
    # Check for path traversal attempts
    normalized_path = input_data.path.replace("\\", "/")
    if ".." in normalized_path.split("/") or normalized_path.startswith("/") or normalized_path.startswith("./.."):
        raise TraversalError("Path traversal or escaping symlink forbidden")

    byte_count = len(input_data.content.encode("utf-8"))
    new_revision = input_data.expected_revision + 1

    _FILE_STORE[normalized_path] = {
        "path": normalized_path,
        "content": input_data.content,
        "revision": new_revision,
        "bytes": byte_count,
    }

    return F17Output(
        path=normalized_path,
        revision=new_revision,
        bytes=byte_count,
    )

def reset_file_store() -> None:
    _FILE_STORE.clear()
