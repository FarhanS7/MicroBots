import pytest
from oap.web.approval_ui import (
    P05Input,
    P05Output,
    ApprovalExpiredError,
    approval_ui,
)

def test_unit_approval_ui_happy_path():
    inp = P05Input(approval_id="approval-1", decision="deny")
    res = approval_ui(inp)
    assert isinstance(res, P05Output)
    assert res.visible_state == "denied"
    assert res.action_executed is False

def test_unit_approval_ui_expired():
    inp = P05Input(approval_id="expired", decision="deny")
    with pytest.raises(ApprovalExpiredError):
        approval_ui(inp)
