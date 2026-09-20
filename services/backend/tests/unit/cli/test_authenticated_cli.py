import pytest
from oap.cli.authenticated_cli import (
    I15Input,
    I15Output,
    authenticated_cli,
)

def test_authenticated_cli_happy_path():
    inp = I15Input(command="agentctl logs task-1", format="json")
    res = authenticated_cli(inp)
    assert res.task_id == "task-1"
    assert res.events == []
    assert res.exit_code == 0

def test_authenticated_cli_expired_credentials():
    inp = I15Input(command="agentctl logs expired", format="json")
    res = authenticated_cli(inp)
    assert res.exit_code == 1
