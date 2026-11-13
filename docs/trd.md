# Technical Requirements Document (TRD) — SkillMatch

## 1. Stack
| Concern | Choice | Reason |
|---|---|---|
| Language | Python 3.11 | Best NLP ecosystem, fast to build |
| UI | Streamlit | A working UI in minutes, no frontend build |
| PDF parsing | pdfplumber | Good text extraction; handles most layouts |
| DOCX parsing | python-docx | Simple, reliable |
| Fuzzy/alias matching | rapidfuzz | Fast, handles typos and variants |
| Semantic similarity | sentence-transformers (all-MiniLM-L6-v2) | Small, runs on CPU, offline once cached |
| Fallback similarity | scikit-learn TF-IDF + cosine | No model download needed |
| Tests / lint | pytest / ruff | Standard |

No database, no external API, no GPU needed.

## 2. Pipeline
```
file bytes -> parsing.extract_text -> utils.text.clean
           -> extraction.extract_skills (taxonomy + aliases + fuzzy)
JD text/preset -> same path
           -> matching.score (coverage + semantic) -> Result
           -> ui renders Result
```

## 3. Data contracts (`src/matching/models.py`)
```python
@dataclass(frozen=True)
class Skill:
    name: str          # canonical, e.g. "Machine Learning"
    category: str      # e.g. "AI/ML", "Web", "Databases"

@dataclass
class SkillHit:
    skill: Skill
    evidence: list[str]     # up to 2 short snippets from the source text

@dataclass
class ScoreBreakdown:
    required_coverage: float     # 0-1
    preferred_coverage: float    # 0-1
    semantic_similarity: float   # 0-1
    final_score: float           # 0-100

@dataclass
class MatchResult:
    matched: list[SkillHit]
    missing: list[Skill]
    extra: list[Skill]
    breakdown: ScoreBreakdown
    method: str                  # "embeddings" or "tfidf"
```

## 4. Module interfaces
| Module | Function | Notes |
|---|---|---|
| `src/pipeline.py` | `analyze_resume(name, data, jd) -> MatchResult` | Orchestrates the local analysis; no UI logic |
| `parsing/pdf_parser.py` | `extract_text_from_pdf(data: bytes) -> str` | Raises `EmptyDocumentError` if no text |
| `parsing/docx_parser.py` | `extract_text_from_docx(data: bytes) -> str` | Should |
| `parsing/validators.py` | `validate_upload(name: str, data: bytes) -> None` | Type, size, magic bytes |
| `extraction/taxonomy.py` | `load_taxonomy(path) -> dict[str, Skill]` | Loads `data/skills.json` (skill, category, aliases) |
| `extraction/extractor.py` | `extract_skills(text: str, taxonomy) -> list[SkillHit]` | Word-boundary match, alias map, fuzzy for typos |
| `extraction/jd_parser.py` | `split_required_preferred(jd: str, taxonomy)` | "Required" vs "Preferred/Good to have" sections |
| `matching/similarity.py` | `semantic_similarity(resume_skills: str, jd_skills: str) -> tuple[float, str]` | Inputs contain only canonical skill labels; exclude personal names and all demographic/contact details before scoring. Identical skill sets must yield equal similarity regardless of those details. Embeddings fall back to TF-IDF; returns method. |
| `matching/scorer.py` | `score(resume_hits, jd_required, jd_preferred, sim) -> MatchResult` | Formula below |
| `ui/app.py` | Streamlit entry point | No business logic |

## 5. Scoring formula
```
if |required| + |preferred| == 0: reject the JD as insufficient information; do not produce a match score
required_coverage  = |matched required| / |required|        (1.0 if no required skills but preferred skills exist)
preferred_coverage = |matched preferred| / |preferred|       (0 if none)
final = 100 * (0.60*required_coverage + 0.20*preferred_coverage + 0.20*semantic_similarity)
```
Weights live in one constant (`WEIGHTS`). If required skills exist but no preferred skills, redistribute that 0.20 to required coverage. Tune only on the tuning set; report evaluation metrics from a separate unseen set after tuning is complete.

## 6. Skill extraction approach
1. Normalize text (lowercase, collapse whitespace, keep `c++`, `c#`, `.net`, `node.js`).
2. Match canonical names and aliases with word boundaries.
3. Fuzzy match (rapidfuzz, threshold ~90) for typos on tokens of 4+ chars.
4. Deduplicate, keep up to 2 evidence snippets per skill (60 chars of surrounding context).
5. Taxonomy: start with ~100-150 skills across Programming, Web, Databases, AI/ML, Cloud, Tools, Soft skills.

## 7. Error handling
`UnsupportedFileError`, `FileTooLargeError`, `EmptyDocumentError`, `ParseError` in `utils/errors.py`. The UI catches these and shows a plain message. Any unexpected exception shows a generic "Something went wrong" message; details go to the log without PII.

## 8. Performance targets
- Cold start with model cached: < 15 s. Analysis per resume: < 5 s.
- Load the embedding model once with `st.cache_resource`.

## 9. Configuration (`.env`)
`MAX_UPLOAD_MB`, `EMBEDDING_MODEL`, `USE_EMBEDDINGS`.

## 10. Testing (details in testing.md)
Unit tests per module; a small evaluation script runs ~20 resumes against 2-3 JDs and prints precision/recall.

## 11. Out of scope now
OCR, LLM calls, accounts, DB, deployment/Docker.
