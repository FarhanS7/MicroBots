import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from oap.models.compatible_provider_adapter import (
    F13Input,
    F13Output,
    compatible_provider_adapter,
)

def test_unit_compatible_provider_adapter_happy_path() -> None:
    inp = F13Input(model_id="model-1", prompt="Say hello", max_output_tokens=20)
    out = compatible_provider_adapter(inp)
    assert out == F13Output(text="Hello", input_tokens=4, output_tokens=1)
