"""Unit tests for toolchain contract verification domain logic."""

import pytest
import os
import tempfile
from oap.domain.toolchain import F01Input, verify_toolchain_contract, PrerequisiteError


def test_verify_toolchain_contract_happy_path() -> None:
    input_data = F01Input(environment="local")
    output = verify_toolchain_contract(input_data)
    assert output.python_locked is True
    assert output.javascript_locked is True
    assert output.docs_check_available is True


def test_verify_toolchain_contract_missing_lockfile() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        input_data = F01Input(environment="local")
        with pytest.raises(PrerequisiteError) as exc_info:
            verify_toolchain_contract(input_data, root_path=temp_dir)
        assert "Required toolchain runtime or lockfile is missing" in str(exc_info.value)
