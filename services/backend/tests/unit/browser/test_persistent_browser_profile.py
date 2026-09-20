import pytest
from oap.browser.persistent_browser_profile import (
    P11Input,
    P11Output,
    ProfileLeaseConflictError,
    persistent_browser_profile,
)

def test_persistent_browser_profile_happy_path():
    inp = P11Input(profile_id="profile-1", persist=True)
    out = persistent_browser_profile(inp, actor_workspace_id="ws-1")
    assert out.reusable is True
    assert out.workspace_id == "ws-1"

def test_persistent_browser_profile_lease_conflict():
    inp = P11Input(profile_id="locked", persist=True)
    with pytest.raises(ProfileLeaseConflictError) as exc_info:
        persistent_browser_profile(inp)
    assert "Active browser profile lease already exists" in str(exc_info.value)
