import pytest
from oap.browser.browser_script_inspection import (
    P25Input,
    P25Output,
    InspectionForbiddenError,
    browser_script_inspection,
)

def test_browser_script_inspection_happy_path():
    inp = P25Input(page_id="page-1", operation="inspect-network")
    out = browser_script_inspection(inp)
    assert out.request_count == 2
    assert out.credentials_redacted is True

def test_browser_script_inspection_forbidden():
    inp = P25Input(page_id="page-1", operation="forbidden")
    with pytest.raises(InspectionForbiddenError) as exc_info:
        browser_script_inspection(inp)
    assert "Script or network inspection capability forbidden" in str(exc_info.value)
