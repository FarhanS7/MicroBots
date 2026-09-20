import pytest
from oap.quality.mvp_recovery_acceptance import (
    P15Input,
    P15Output,
    LoginDeniedError,
    mvp_recovery_acceptance,
)

def test_mvp_recovery_acceptance_happy_path():
    inp = P15Input(scenario="five-database-projects", disconnect_client=True, restart_worker=True)
    out = mvp_recovery_acceptance(inp)
    assert out.artifact_valid is True
    assert out.conversation_persisted is True
    assert out.duplicate_effects == 0

def test_mvp_recovery_acceptance_denied():
    inp = P15Input(scenario="denied", disconnect_client=True, restart_worker=True)
    with pytest.raises(LoginDeniedError) as exc_info:
        mvp_recovery_acceptance(inp)
    assert "External login request was denied" in str(exc_info.value)
