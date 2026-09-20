import pytest
from oap.tasks.task_control import (
    P06Input,
    P06Output,
    TaskControlError,
    task_control,
)

def test_unit_task_control_happy_path():
    inp = P06Input(task_id="task-1", action="cancel", expected_revision=2)
    res = task_control(inp)
    assert isinstance(res, P06Output)
    assert res.task_id == "task-1"
    assert res.cancellation_requested is True

def test_unit_task_control_conflict():
    inp = P06Input(task_id="task-1", action="cancel", expected_revision=0)
    with pytest.raises(TaskControlError):
        task_control(inp)
