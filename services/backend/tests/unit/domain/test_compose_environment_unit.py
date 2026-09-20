"""Unit tests for Compose environment domain validation logic."""

import pytest
import os
import tempfile
from oap.domain.compose import F03Input, compose_environment, ConfigError


def test_compose_environment_happy_path() -> None:
    input_data = F03Input(profile="local")
    output = compose_environment(input_data)
    assert output.ready is True
    assert output.persistent_volumes is True


def test_compose_environment_missing_compose_file() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        input_data = F03Input(profile="local")
        with pytest.raises(ConfigError) as exc_info:
            compose_environment(input_data, root_path=temp_dir)
        assert "docker-compose.yml configuration file missing" in str(exc_info.value)
