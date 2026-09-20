import pytest
from oap.marketplace.package_update_rollback import (
    I11Input,
    I11Output,
    UnapprovedPermissionError,
    package_update_rollback,
)

def test_package_update_rollback_happy_path():
    inp = I11Input(
        package_id="package-1",
        target_version="1.1.0",
        approved_permissions=["browser.read"],
    )
    res = package_update_rollback(inp)
    assert res.installed_version == "1.1.0"
    assert res.rollback_version == "1.0.0"

def test_package_update_rollback_unapproved_permission():
    inp = I11Input(
        package_id="unapproved_perm_package",
        target_version="1.1.0",
        approved_permissions=["browser.read"],
    )
    with pytest.raises(UnapprovedPermissionError):
        package_update_rollback(inp)
