import pytest
from oap.browser.structured_browser_tools import (
    F19Input,
    F19Output,
    PrivateNetworkBlockedError,
    structured_browser_tools,
    reset_browser_store,
)

def setup_function():
    reset_browser_store()

def test_unit_browser_tools_happy_path():
    inp = F19Input(url="https://fixture.example.test/report")
    res = structured_browser_tools(inp)
    assert isinstance(res, F19Output)
    assert res.page_id == "page-1"
    assert res.title == "Fixture report"
    assert res.text == "Revenue increased."

def test_unit_browser_tools_ssrf_blocked():
    inp = F19Input(url="http://169.254.169.254/latest/meta-data/")
    with pytest.raises(PrivateNetworkBlockedError):
        structured_browser_tools(inp)
