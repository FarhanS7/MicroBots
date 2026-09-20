import pytest
from oap.plugins.typescript_sdk import (
    I07Input,
    IncompatibleProtocolError,
    typescript_sdk,
)

def test_typescript_sdk_happy_path():
    inp = I07Input(
        sdk_language="typescript",
        fixture="read-record"
    )
    res = typescript_sdk(inp)
    assert res.schema_valid is True
    assert res.contract_tests_passed is True

def test_typescript_sdk_incompatible_version():
    inp = I07Input(
        sdk_language="typescript",
        fixture="incompatible-version"
    )
    with pytest.raises(IncompatibleProtocolError):
        typescript_sdk(inp)
