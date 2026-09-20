import pytest
from oap.marketplace.catalog_provenance import (
    I10Input,
    WithdrawnPackageError,
    catalog_provenance,
)

def test_catalog_provenance_happy_path():
    inp = I10Input(
        query="research",
        package_type="skill"
    )
    res = catalog_provenance(inp)
    assert res.package_ids == ["package-1"]
    assert res.next_cursor is None

def test_catalog_provenance_withdrawn_malicious():
    inp = I10Input(
        query="withdrawn_malicious",
        package_type="skill"
    )
    with pytest.raises(WithdrawnPackageError):
        catalog_provenance(inp)
