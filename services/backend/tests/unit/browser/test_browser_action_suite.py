import pytest
from oap.browser.browser_action_suite import (
    P12Input,
    P12Output,
    UserChallengeRequiredError,
    browser_action_suite,
)

def test_browser_action_suite_happy_path():
    inp = P12Input(page_id="page-1", action="click", target="fixture-button")
    out = browser_action_suite(inp)
    assert out.clicked is True
    assert out.page_revision == 2

def test_browser_action_suite_captcha_challenge():
    inp = P12Input(page_id="page-1", action="click", target="captcha")
    with pytest.raises(UserChallengeRequiredError) as exc_info:
        browser_action_suite(inp)
    assert "Login challenge requires user interaction" in str(exc_info.value)
