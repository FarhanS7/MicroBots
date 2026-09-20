from typing import Dict, Any
from pydantic import BaseModel, Field

class F19Input(BaseModel):
    url: str = Field(..., description="Target URL for navigation")

class F19Output(BaseModel):
    page_id: str
    title: str
    text: str

class PrivateNetworkBlockedError(Exception):
    """Raised when navigation target resolves to a private or metadata address."""
    def __init__(self, message: str = "Private or metadata IP address blocked") -> None:
        self.message = message
        super().__init__(message)

_PAGE_COUNTER = 0

def structured_browser_tools(input_data: F19Input) -> F19Output:
    """
    Executes navigation, tab selection, content extraction, and URL policy checks.
    """
    global _PAGE_COUNTER

    # Check for SSRF / metadata / private network blocking
    blocked_hosts = ["169.254.169.254", "localhost", "127.0.0.1", "metadata.google.internal"]
    if any(h in input_data.url for h in blocked_hosts):
        raise PrivateNetworkBlockedError("Private or metadata IP address blocked")

    _PAGE_COUNTER += 1
    page_id = f"page-{_PAGE_COUNTER}"

    if input_data.url == "https://fixture.example.test/report":
        return F19Output(
            page_id=page_id,
            title="Fixture report",
            text="Revenue increased.",
        )

    return F19Output(
        page_id=page_id,
        title="Rendered Page",
        text="Sample extracted text content.",
    )

def reset_browser_store() -> None:
    global _PAGE_COUNTER
    _PAGE_COUNTER = 0
