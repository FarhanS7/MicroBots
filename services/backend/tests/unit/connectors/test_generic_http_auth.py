import pytest
from oap.connectors.generic_http_auth import (
    I04Input,
    HeaderStrippingRedirectError,
    generic_http_auth,
)

def test_generic_http_auth_happy_path():
    inp = I04Input(
        connector_id="connector-1",
        method="GET",
        path="/records"
    )
    res = generic_http_auth(inp)
    assert res.status == 200
    assert res.body == {"items": []}

def test_generic_http_auth_cross_origin_redirect():
    inp = I04Input(
        connector_id="connector-1",
        method="GET",
        path="/cross-origin-redirect"
    )
    with pytest.raises(HeaderStrippingRedirectError):
        generic_http_auth(inp)
