import pytest
from oap.workflows.hybrid_workflow_runner import (
    A05Input,
    A05Output,
    hybrid_workflow_runner,
)

def test_hybrid_workflow_runner_happy_path():
    inp = A05Input(workflow_id="workflow-1", version=1, input={"topic": "databases"})
    out = hybrid_workflow_runner(inp)
    assert out.run_id == "workflow-run-1"
    assert out.state == "waiting_approval"
