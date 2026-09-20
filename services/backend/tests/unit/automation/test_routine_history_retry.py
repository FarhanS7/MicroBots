import pytest
from oap.automation.routine_history_retry import (
    A09Input,
    routine_history_retry,
)

def test_routine_history_retry_happy_path():
    inp = A09Input(
        execution_id="execution-1",
        failure_code="PROVIDER_UNAVAILABLE",
        attempt=1
    )
    res = routine_history_retry(inp)
    assert res.retry_scheduled is True
    assert res.next_attempt == 2

def test_routine_history_retry_non_retryable():
    inp = A09Input(
        execution_id="execution-1",
        failure_code="UNKNOWN_EXTERNAL_RESULT",
        attempt=1
    )
    res = routine_history_retry(inp)
    assert res.retry_scheduled is False
    assert res.next_attempt == 1
