import pytest
from oap.execution.background_process_control import (
    P29Input,
    P29Output,
    ProcessNotFoundError,
    background_process_control,
)

def test_background_process_control_happy_path():
    inp = P29Input(command="fixture-long-process", background=True, timeout_seconds=30)
    out = background_process_control(inp)
    assert out.process_id == "process-1"
    assert out.state == "running"

def test_background_process_control_not_found():
    inp = P29Input(command="foreign-process", background=True, timeout_seconds=30)
    with pytest.raises(ProcessNotFoundError) as exc_info:
        background_process_control(inp)
    assert "Background process not found" in str(exc_info.value)
