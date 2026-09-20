import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from oap.identity.workspace_authorization import (
    F07Input,
    F07Output,
    NotFoundError,
    workspace_authorization,
)

def test_unit_workspace_authorization_happy_path() -> None:
    inp = F07Input(resource_workspace_id="ws-1")
    out = workspace_authorization(inp, actor_workspace_id="ws-1")
    assert out == F07Output(authorized=True)

def test_unit_workspace_authorization_cross_tenant_forbidden() -> None:
    inp = F07Input(resource_workspace_id="ws-1")
    with pytest.raises(NotFoundError):
        workspace_authorization(inp, actor_workspace_id="ws-2")
