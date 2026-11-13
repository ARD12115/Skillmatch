import pytest

from src.matching.models import Skill, SkillHit
from src.matching.scorer import score


def hit(name):
    return SkillHit(Skill(name, "Test"), [f"Worked with {name}."])


def test_all_required_and_preferred_skills_match():
    result = score(
        [hit("Python"), hit("Docker")],
        [hit("Python")],
        [hit("Docker")],
        semantic_similarity=1.0,
    )

    assert result.breakdown.final_score == pytest.approx(100)
    assert {item.skill.name for item in result.matched} == {"Python", "Docker"}
    assert result.missing == []


def test_closer_resume_scores_higher_and_reports_missing_and_extra():
    required = [hit("Python"), hit("SQL")]
    close = score([hit("Python"), hit("SQL"), hit("Git")], required, [])
    far = score([hit("Java")], required, [])

    assert close.breakdown.final_score > far.breakdown.final_score
    assert [item.name for item in close.extra] == ["Git"]
    assert {item.name for item in far.missing} == {"Python", "SQL"}


def test_empty_requirements_and_preferred_redistribution():
    no_requirements = score([hit("Python")], [], [], semantic_similarity=0)
    preferred_only = score(
        [hit("Python")], [], [hit("Python")], semantic_similarity=0.5
    )

    assert no_requirements.breakdown.required_coverage == 1.0
    assert no_requirements.breakdown.final_score == pytest.approx(80)
    assert preferred_only.breakdown.preferred_coverage == 1.0
    assert preferred_only.breakdown.final_score == pytest.approx(90)


def test_semantic_similarity_must_be_in_range():
    with pytest.raises(ValueError, match="between 0 and 1"):
        score([], [], [], semantic_similarity=1.2)
