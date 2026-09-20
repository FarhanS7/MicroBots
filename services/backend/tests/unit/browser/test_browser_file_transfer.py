import pytest
from oap.browser.browser_file_transfer import (
    P24Input,
    P24Output,
    UnapprovedDestinationError,
    browser_file_transfer,
)

def test_browser_file_transfer_happy_path():
    inp = P24Input(page_id="page-1", action="download", target="fixture-report")
    out = browser_file_transfer(inp)
    assert out.file_id == "file-1"
    assert out.quarantined is True

def test_browser_file_transfer_unapproved():
    inp = P24Input(page_id="page-1", action="download", target="unapproved")
    with pytest.raises(UnapprovedDestinationError) as exc_info:
        browser_file_transfer(inp)
    assert "Destination not approved by policy" in str(exc_info.value)
