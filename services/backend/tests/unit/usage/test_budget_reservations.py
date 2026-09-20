import pytest
from oap.usage.budget_reservations import (
    P08Input,
    P08Output,
    BudgetExceededError,
    budget_reservations,
)

def test_unit_budget_reservations_happy_path():
    inp = P08Input(budget_micro_usd=1000, reserved_micro_usd=200, requested_micro_usd=300)
    res = budget_reservations(inp)
    assert isinstance(res, P08Output)
    assert res.allowed is True
    assert res.reserved_micro_usd == 500

def test_unit_budget_reservations_exceeded():
    inp = P08Input(budget_micro_usd=1000, reserved_micro_usd=900, requested_micro_usd=300)
    with pytest.raises(BudgetExceededError):
        budget_reservations(inp)
