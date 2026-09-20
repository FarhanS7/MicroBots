import pytest
from oap.policy.approval_request import (
    P03Input,
    P03Output,
    InvalidApprovalError,
    approval_request,
    reset_approval_store,
)

def setup_function():
    reset_approval_store()

def test_unit_approval_request_happy_path():
    inp = P03Input(
        task_id="task-1",
        action="external.publish",
        target="fixture-post",
        expires_in_seconds=3600,
    )
    res = approval_request(inp)
    assert isinstance(res, P03Output)
    assert res.approval_id == "approval-1"
    assert res.state == "pending"

def test_unit_approval_request_invalid():
    inp = P03Input(
        task_id="task-1",
        action="external.publish",
        target="fixture-post",
        expires_in_seconds=0,
    )
    with pytest.raises(InvalidApprovalError):
        approval_request(inp)
