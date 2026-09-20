import pytest
from oap.connectors.openapi_import import (
    I03Input,
    OpenAPIImportError,
    openapi_import,
)

def test_openapi_import_happy_path():
    inp = I03Input(
        spec_id="spec-1",
        operation_ids=["listRecords"]
    )
    res = openapi_import(inp)
    assert res.tool_names == ["crm.listRecords"]
    assert res.enabled is False

def test_openapi_import_private_ref():
    inp = I03Input(
        spec_id="private_spec",
        operation_ids=["listRecords"]
    )
    with pytest.raises(OpenAPIImportError):
        openapi_import(inp)
