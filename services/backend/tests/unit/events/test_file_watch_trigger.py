import pytest
from oap.events.file_watch_trigger import (
    A15Input,
    file_watch_trigger,
)

def test_file_watch_trigger_happy_path():
    inp = A15Input(
        file_id="file-1",
        revision=2
    )
    res = file_watch_trigger(inp)
    assert res.event_type == "file.created"
    assert res.delivery_count == 1

def test_file_watch_trigger_replay():
    inp = A15Input(
        file_id="file-1",
        revision=2
    )
    res = file_watch_trigger(inp)
    assert res.event_type == "file.unchanged"
    assert res.delivery_count == 0
