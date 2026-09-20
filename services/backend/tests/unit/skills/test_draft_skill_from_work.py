import pytest
from oap.skills.draft_skill_from_work import (
    A03Input,
    A03Output,
    draft_skill_from_work,
)

def test_draft_skill_from_work_happy_path():
    inp = A03Input(source_task_id="task-1", name="research-report")
    out = draft_skill_from_work(inp)
    assert out.draft_id == "draft-1"
    assert out.active is False
