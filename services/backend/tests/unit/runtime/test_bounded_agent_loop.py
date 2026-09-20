import pytest
from oap.runtime.bounded_agent_loop import (
    F20Input,
    F20Output,
    BudgetExceededError,
    bounded_agent_loop,
)

def test_unit_bounded_agent_loop_happy_path():
    inp = F20Input(task_id="task-1", max_steps=10)
    res = bounded_agent_loop(inp)
    assert isinstance(res, F20Output)
    assert res.task_id == "task-1"
    assert res.state == "completed"
    assert res.artifact_ids == ["artifact-1"]

def test_unit_bounded_agent_loop_budget_exceeded():
    inp = F20Input(task_id="task-1", max_steps=0)
    with pytest.raises(BudgetExceededError):
        bounded_agent_loop(inp)
