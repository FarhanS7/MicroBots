import pytest
from oap.plugins.python_sdk import (
    I08Input,
    SDKPayloadMismatchError,
    python_sdk,
)

def test_python_sdk_happy_path():
    inp = I08Input(
        sdk_language="python",
        fixture="read-record"
    )
    res = python_sdk(inp)
    assert res.schema_valid is True
    assert res.contract_tests_passed is True

def test_python_sdk_incompatible_payload():
    inp = I08Input(
        sdk_language="python",
        fixture="incompatible-payload"
    )
    with pytest.raises(SDKPayloadMismatchError):
        python_sdk(inp)
