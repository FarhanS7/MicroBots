import pytest
from oap.quality.research_prototype_evaluation import (
    F25Input,
    F25Output,
    EvaluationFailedError,
    research_prototype_evaluation,
)

def test_unit_research_prototype_evaluation_happy_path():
    inp = F25Input(fixture_count=10, live_count=5)
    res = research_prototype_evaluation(inp)
    assert isinstance(res, F25Output)
    assert res.fixture_pass_required == 10
    assert res.live_pass_required == 4
    assert res.forbidden_actions_allowed == 0

def test_unit_research_prototype_evaluation_failure():
    inp = F25Input(fixture_count=0, live_count=0)
    with pytest.raises(EvaluationFailedError):
        research_prototype_evaluation(inp)
