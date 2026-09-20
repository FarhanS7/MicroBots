import pytest
from oap.web.skill_authoring_ui import (
    A16Input,
    DraftValidationError,
    skill_authoring_ui,
)

def test_skill_authoring_ui_happy_path():
    inp = A16Input(
        draft_id="draft-1",
        action="review"
    )
    res = skill_authoring_ui(inp)
    assert res.active is False
    assert res.required_tools_visible is True

def test_skill_authoring_ui_activate_invalid():
    inp = A16Input(
        draft_id="draft-1",
        action="activate_invalid"
    )
    with pytest.raises(DraftValidationError):
        skill_authoring_ui(inp)
