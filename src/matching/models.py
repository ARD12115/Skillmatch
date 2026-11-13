from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    name: str
    category: str


@dataclass(frozen=True)
class SkillHit:
    skill: Skill
    evidence: list[str]


@dataclass(frozen=True)
class ScoreBreakdown:
    required_coverage: float
    preferred_coverage: float
    semantic_similarity: float
    final_score: float


@dataclass(frozen=True)
class MatchResult:
    matched: list[SkillHit]
    missing: list[Skill]
    extra: list[Skill]
    breakdown: ScoreBreakdown
    method: str
