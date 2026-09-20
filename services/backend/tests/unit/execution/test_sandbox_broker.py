import pytest
from oap.execution.sandbox_broker import (
    F16Input,
    F16Output,
    ForbiddenGrantError,
    sandbox_broker,
    reset_computers_store,
)

def setup_function():
    reset_computers_store()

def test_unit_sandbox_broker_happy_path():
    inp = F16Input(
        task_id="task-1",
        workspace_id="ws-1",
        image="fixture-pinned-image",
    )
    res = sandbox_broker(inp, actor_workspace_id="ws-1")
    assert isinstance(res, F16Output)
    assert res.computer_id == "computer-1"
    assert res.state == "ready"

def test_unit_sandbox_broker_forbidden_grant():
    inp = F16Input(
        task_id="task-1",
        workspace_id="ws-1",
        image="fixture-pinned-image",
    )
    with pytest.raises(ForbiddenGrantError):
        sandbox_broker(inp, actor_workspace_id="ws-other")
