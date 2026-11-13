import re
from collections.abc import Mapping

from rapidfuzz import fuzz, process

from src.matching.models import Skill, SkillHit
from src.utils.text import normalize_text

FUZZY_THRESHOLD = 92
MAX_EVIDENCE = 2
EVIDENCE_RADIUS = 60


def _term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(normalize_text(term))
    return re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE)


def _evidence(text: str, start: int, end: int) -> str:
    left = max(0, start - EVIDENCE_RADIUS)
    right = min(len(text), end + EVIDENCE_RADIUS)
    return re.sub(r"\s+", " ", text[left:right]).strip()


def extract_skills(text: str, taxonomy: Mapping[str, Skill]) -> list[SkillHit]:
    """Find canonical skills and aliases, retaining concise source evidence."""
    if not text.strip():
        return []

    hits: dict[str, tuple[Skill, list[str]]] = {}
    for term, skill in taxonomy.items():
        for match in _term_pattern(term).finditer(text):
            key = skill.name.casefold()
            hit = hits.setdefault(key, (skill, []))
            snippet = _evidence(text, match.start(), match.end())
            if snippet not in hit[1] and len(hit[1]) < MAX_EVIDENCE:
                hit[1].append(snippet)

    # Fuzzy matching is limited to complete tokens to avoid matching substrings
    # inside unrelated words.
    known_terms = list(taxonomy)
    for token_match in re.finditer(r"(?<!\w)[A-Za-z][A-Za-z0-9+#.]{3,}(?!\w)", text):
        token = token_match.group(0).casefold()
        candidate = process.extractOne(token, known_terms, scorer=fuzz.ratio)
        if candidate is None or candidate[1] < FUZZY_THRESHOLD:
            continue
        skill = taxonomy[candidate[0]]
        key = skill.name.casefold()
        hit = hits.setdefault(key, (skill, []))
        snippet = _evidence(text, token_match.start(), token_match.end())
        if snippet not in hit[1] and len(hit[1]) < MAX_EVIDENCE:
            hit[1].append(snippet)

    return [
        SkillHit(skill=skill, evidence=evidence) for skill, evidence in hits.values()
    ]
