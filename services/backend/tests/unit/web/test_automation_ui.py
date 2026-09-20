import pytest
from oap.web.automation_ui import (
    A13Input,
    InvalidAutomationUIError,
    automation_ui,
)

def test_automation_ui_happy_path():
    inp = A13Input(
        routine_id="routine-1",
        action="pause"
    )
    res = automation_ui(inp)
    assert res.visible_state == "paused"
    assert res.next_run is None

def test_automation_ui_unconfirmed_draft():
    inp = A13Input(
        routine_id="routine-1",
        action="unconfirmed_schedule"
    )
    res = automation_ui(inp)
    assert res.visible_state == "draft"
    assert res.next_run is None
