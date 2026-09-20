import pytest
from oap.web.usage_budget_ui import (
    P20Input,
    P20Output,
    usage_budget_ui,
)

def test_usage_budget_ui_happy_path():
    inp = P20Input(task_id="task-1")
    out = usage_budget_ui(inp)
    assert out.spent_micro_usd == 100
    assert out.reserved_micro_usd == 200
    assert out.cost_known is True

def test_usage_budget_ui_unknown_cost():
    inp = P20Input(task_id="unknown_cost")
    out = usage_budget_ui(inp)
    assert out.cost_known is False
