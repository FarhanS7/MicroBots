import pytest
from oap.execution.package_install_policy import (
    P22Input,
    P22Output,
    PackageInstallForbiddenError,
    package_install_policy,
)

def test_package_install_policy_happy_path():
    inp = P22Input(manager="pip", package="fixture-package", environment="sandbox-1")
    out = package_install_policy(inp)
    assert out.installed is True
    assert out.host_modified is False

def test_package_install_policy_forbidden():
    inp = P22Input(manager="pip", package="forbidden", environment="sandbox-1")
    with pytest.raises(PackageInstallForbiddenError) as exc_info:
        package_install_policy(inp)
    assert "Package installation forbidden" in str(exc_info.value)
