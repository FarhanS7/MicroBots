import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from oap.tasks.durable_task_submission import (
    F14Input,
    F14Output,
    TaskIdempotencyConflictError,
    durable_task_submission,
    reset_tasks_store,
)

def setup_function() -> None:
    reset_tasks_store()

def test_unit_durable_task_submission_happy_path() -> None:
    inp = F14Input(
        agent_id="agent-1",
        instruction="Research three competitors",
        idempotency_key="request-1",
    )
    out = durable_task_submission(inp)
    assert out == F14Output(task_id="task-1", state="queued", revision=1)

def test_unit_durable_task_submission_idempotency_conflict() -> None:
    inp1 = F14Input(agent_id="agent-1", instruction="Instruction A", idempotency_key="request-1")
    durable_task_submission(inp1)
    inp2 = F14Input(agent_id="agent-1", instruction="Instruction B", idempotency_key="request-1")
    with pytest.raises(TaskIdempotencyConflictError):
        durable_task_submission(inp2)
