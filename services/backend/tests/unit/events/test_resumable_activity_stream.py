import pytest
from oap.events.resumable_activity_stream import (
    F22Input,
    F22Output,
    ResyncRequiredError,
    resumable_activity_stream,
)

def test_unit_resumable_activity_stream_happy_path():
    inp = F22Input(after=4, workspace_id="ws-1")
    res = resumable_activity_stream(inp)
    assert isinstance(res, F22Output)
    assert res.sequences == [5, 6]
    assert res.next_cursor == 6

def test_unit_resumable_activity_stream_resync_required():
    inp = F22Input(after=0, workspace_id="ws-resync")
    with pytest.raises(ResyncRequiredError):
        resumable_activity_stream(inp)
