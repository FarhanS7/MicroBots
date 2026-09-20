import pytest
from oap.skills.skill_package_schema import (
    A01Input,
    A01Output,
    InvalidSkillManifestError,
    skill_package_schema,
)

def test_skill_package_schema_happy_path():
    inp = A01Input(name="daily-brief", version="1.0.0", required_tools=["browser.read"])
    out = skill_package_schema(inp)
    assert out.valid is True
    assert out.skill_id == "skill-1"

def test_skill_package_schema_invalid():
    inp = A01Input(name="daily-brief", version="1.0.0", required_tools=["unknown_tool"])
    with pytest.raises(InvalidSkillManifestError) as exc_info:
        skill_package_schema(inp)
    assert "Invalid skill package manifest" in str(exc_info.value)
