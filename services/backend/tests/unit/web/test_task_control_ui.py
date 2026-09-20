import pytest
from oap.web.task_control_ui import (
    P23Input,
    P23Output,
    task_control_ui,
)

def test_task_control_ui_happy_path():
    inp = P23Input(task_id="task-1", action="cancel")
    out = task_control_ui(inp)
    assert out.visible_state == "cancellation-requested"

def test_task_control_ui_pause():
    inp = P23Input(task_id="task-1", action="pause")
    out = task_control_ui(inp)
    assert out.visible_state == "paused"
