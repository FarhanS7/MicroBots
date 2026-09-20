import pytest
from oap.runtime.crash_recovery import (
    P07Input,
    P07Output,
    OutcomeUnknownError,
    crash_recovery,
)

def test_unit_crash_recovery_happy_path():
    inp = P07Input(task_id="task-1", checkpoint="after-tool-result")
    res = crash_recovery(inp)
    assert isinstance(res, P07Output)
    assert res.resumed is True
    assert res.duplicate_external_effects == 0

def test_unit_crash_recovery_unknown_outcome():
    inp = P07Input(task_id="task-1", checkpoint="unknown")
    with pytest.raises(OutcomeUnknownError):
        crash_recovery(inp)
