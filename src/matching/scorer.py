from collections.abc import Sequence
from math import isfinite

from src.matching.models import MatchResult, ScoreBreakdown, Skill, SkillHit

WEIGHTS = {
    "required": 0.60,
    "preferred": 0.20,
    "semantic": 0.20,
}


def score(
    resume_hits: Sequence[SkillHit],
    jd_required: Sequence[SkillHit | Skill],
    jd_preferred: Sequence[SkillHit | Skill],
    semantic_similarity: float = 0.0,
    method: str = "tfidf",
) -> MatchResult:
    """Score required/preferred skill coverage and semantic similarity."""
    if not isfinite(semantic_similarity) or not 0.0 <= semantic_similarity <= 1.0:
        raise ValueError("semantic_similarity must be between 0 and 1.")

    def as_skill(item: SkillHit | Skill) -> Skill:
        return item.skill if isinstance(item, SkillHit) else item

    resume_by_name = {hit.skill.name.casefold(): hit for hit in resume_hits}
    required = {as_skill(item).name.casefold(): as_skill(item) for item in jd_required}
    required_names = set(required)
    preferred = {
        as_skill(item).name.casefold(): as_skill(item)
        for item in jd_preferred
        if as_skill(item).name.casefold() not in required_names
    }
    preferred_names = set(preferred)
    matched_required = required_names & resume_by_name.keys()
    matched_preferred = preferred_names & resume_by_name.keys()
    required_coverage = (
        len(matched_required) / len(required_names) if required_names else 1.0
    )
    preferred_coverage = (
        len(matched_preferred) / len(preferred_names) if preferred_names else 0.0
    )

    required_weight = WEIGHTS["required"]
    preferred_weight = WEIGHTS["preferred"]
    if not preferred_names:
        required_weight += preferred_weight
        preferred_weight = 0.0
    final_score = 100 * (
        required_weight * required_coverage
        + preferred_weight * preferred_coverage
        + WEIGHTS["semantic"] * semantic_similarity
    )

    jd_names = required_names | preferred_names
    matched_names = (matched_required | matched_preferred)
    matched = [resume_by_name[name] for name in resume_by_name if name in matched_names]
    missing = [
        skill
        for name, skill in [*required.items(), *preferred.items()]
        if name not in resume_by_name
    ]
    extra = [
        hit.skill for name, hit in resume_by_name.items() if name not in jd_names
    ]
    breakdown = ScoreBreakdown(
        required_coverage=required_coverage,
        preferred_coverage=preferred_coverage,
        semantic_similarity=semantic_similarity,
        final_score=round(min(100.0, max(0.0, final_score)), 2),
    )
    return MatchResult(
        matched=matched,
        missing=missing,
        extra=extra,
        breakdown=breakdown,
        method=method,
    )
