import pytest
from oap.connectors.oauth_lifecycle import (
    I05Input,
    InvalidOAuthStateError,
    oauth_lifecycle,
)

def test_oauth_lifecycle_happy_path():
    inp = I05Input(
        connector_id="connector-1",
        callback_state="fixture-state",
        code="fixture-code"
    )
    res = oauth_lifecycle(inp)
    assert res.connected is True
    assert res.secret_id == "oauth-secret-1"

def test_oauth_lifecycle_wrong_state():
    inp = I05Input(
        connector_id="connector-1",
        callback_state="wrong-state",
        code="fixture-code"
    )
    with pytest.raises(InvalidOAuthStateError):
        oauth_lifecycle(inp)
