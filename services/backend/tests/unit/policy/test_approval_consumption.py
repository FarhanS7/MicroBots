import pytest
from oap.policy.approval_consumption import (
    P04Input,
    P04Output,
    RevisionConflictError,
    approval_consumption,
)

def test_unit_approval_consumption_happy_path():
    inp = P04Input(
        approval_id="approval-1",
        decision="approve_once",
        expected_revision=1,
    )
    res = approval_consumption(inp)
    assert isinstance(res, P04Output)
    assert res.state == "approved"
    assert res.revision == 2

def test_unit_approval_consumption_conflict():
    inp = P04Input(
        approval_id="approval-1",
        decision="approve_once",
        expected_revision=0,
    )
    with pytest.raises(RevisionConflictError):
        approval_consumption(inp)
