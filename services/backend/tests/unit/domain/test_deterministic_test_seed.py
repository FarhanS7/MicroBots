import pytest
from oap.domain.deterministic_test_seed import (
    F26Input,
    F26Output,
    ProductionRefusalError,
    deterministic_test_seed,
)

def test_unit_deterministic_test_seed_happy_path():
    inp = F26Input(environment="test", seed="research-v1")
    res = deterministic_test_seed(inp)
    assert isinstance(res, F26Output)
    assert res.seeded is True
    assert res.duplicate_rows == 0

def test_unit_deterministic_test_seed_production_refused():
    inp = F26Input(environment="production", seed="research-v1")
    with pytest.raises(ProductionRefusalError):
        deterministic_test_seed(inp)
