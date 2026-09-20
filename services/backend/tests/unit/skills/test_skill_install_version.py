import pytest
from oap.skills.skill_install_version import (
    A02Input,
    A02Output,
    UnsafeArchiveError,
    skill_install_version,
)

def test_skill_install_version_happy_path():
    inp = A02Input(package="fixture-daily-brief", version="1.0.0")
    out = skill_install_version(inp)
    assert out.installed_version == "1.0.0"
    assert out.enabled is False

def test_skill_install_version_unsafe():
    inp = A02Input(package="traversal-archive", version="1.0.0")
    with pytest.raises(UnsafeArchiveError) as exc_info:
        skill_install_version(inp)
    assert "Unsafe archive or expanded permissions rejected" in str(exc_info.value)
