import logging
from functools import lru_cache
from pathlib import Path

from src.extraction.extractor import extract_skills
from src.extraction.jd_parser import split_required_preferred
from src.extraction.taxonomy import load_taxonomy
from src.matching.models import MatchResult, Skill
from src.matching.scorer import score
from src.matching.similarity import semantic_similarity
from src.parsing.docx_parser import extract_text_from_docx
from src.parsing.pdf_parser import extract_text_from_pdf
from src.parsing.validators import validate_upload
from src.utils.errors import SkillMatchError

ROOT = Path(__file__).resolve().parents[1]
LOGGER = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load_taxonomy() -> dict[str, Skill]:
    return load_taxonomy(ROOT / "data" / "skills.json")


def _read_resume(name: str, data: bytes) -> str:
    validate_upload(name, data)
    suffix = Path(name).suffix.casefold()
    if suffix == ".pdf":
        return extract_text_from_pdf(data)
    if suffix == ".docx":
        return extract_text_from_docx(data)
    raise SkillMatchError("Upload a PDF or DOCX resume.")


def analyze_resume(name: str, data: bytes, jd: str) -> MatchResult:
    """Run the local resume-to-job matching pipeline for one upload."""
    resume_text = _read_resume(name, data)
    taxonomy = _load_taxonomy()
    resume_hits = extract_skills(resume_text, taxonomy)
    requirements = split_required_preferred(jd, taxonomy)
    if not requirements.required and not requirements.preferred:
        raise SkillMatchError(
            "No recognized skills were found in this job description. "
            "Try a more detailed JD or a preset role."
        )
    resume_skill_text = " ".join(hit.skill.name for hit in resume_hits)
    jd_skill_text = " ".join(
        hit.skill.name for hit in requirements.required + requirements.preferred
    )
    similarity, method = semantic_similarity(resume_skill_text, jd_skill_text)
    result = score(
        resume_hits,
        requirements.required,
        requirements.preferred,
        similarity,
        method,
    )
    LOGGER.info(
        "Analysis complete: parsed resume and identified %d skills.", len(resume_hits)
    )
    return result
