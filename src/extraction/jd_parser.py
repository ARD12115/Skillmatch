import re
from collections.abc import Mapping
from dataclasses import dataclass

from src.extraction.extractor import extract_skills
from src.matching.models import Skill, SkillHit

_REQUIRED_HEADING = re.compile(
    r"^\s*(?:required(?:\s+skills|\s+qualifications)?|skills\s+required|"
    r"must[- ]have|requirements)\s*:?\s*(.*)$",
    re.IGNORECASE,
)
_PREFERRED_HEADING = re.compile(
    r"^\s*(?:preferred(?:\s+skills|\s+qualifications)?|skills\s+preferred|"
    r"nice[- ]to[- ]have|good[- ]to[- ]have|bonus(?:\s+skills)?)\s*:?\s*(.*)$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class JDRequirements:
    required: list[SkillHit]
    preferred: list[SkillHit]


def split_required_preferred(jd: str, taxonomy: Mapping[str, Skill]) -> JDRequirements:
    """Split a job description by explicit section headings and extract skills."""
    lines = jd.splitlines()
    required_lines: list[str] = []
    preferred_lines: list[str] = []
    section: str | None = None
    has_headings = False

    for line in lines:
        required_heading = _REQUIRED_HEADING.match(line)
        preferred_heading = _PREFERRED_HEADING.match(line)
        if required_heading:
            section = "required"
            has_headings = True
            if required_heading.group(1).strip():
                required_lines.append(required_heading.group(1))
        elif preferred_heading:
            section = "preferred"
            has_headings = True
            if preferred_heading.group(1).strip():
                preferred_lines.append(preferred_heading.group(1))
        elif section == "required":
            required_lines.append(line)
        elif section == "preferred":
            preferred_lines.append(line)

    if not has_headings:
        required_lines = lines

    required = extract_skills("\n".join(required_lines), taxonomy)
    preferred = extract_skills("\n".join(preferred_lines), taxonomy)
    required_names = {hit.skill.name.casefold() for hit in required}
    preferred = [
        hit for hit in preferred if hit.skill.name.casefold() not in required_names
    ]
    return JDRequirements(required=required, preferred=preferred)
