import pytest
from oap.workflows.workflow_definition import (
    A04Input,
    A04Output,
    UnboundedCycleError,
    workflow_definition,
)

def test_workflow_definition_happy_path():
    inp = A04Input(nodes=["fetch", "summarize", "approve"], edges=[["fetch", "summarize"], ["summarize", "approve"]])
    out = workflow_definition(inp)
    assert out.valid is True
    assert out.workflow_version == 1

def test_workflow_definition_unbounded_cycle():
    inp = A04Input(nodes=["fetch", "loop"], edges=[["loop", "loop"]])
    with pytest.raises(UnboundedCycleError) as exc_info:
        workflow_definition(inp)
    assert "Unbounded cycle detected" in str(exc_info.value)
