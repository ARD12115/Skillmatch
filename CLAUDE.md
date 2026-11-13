# CLAUDE.md — SkillMatch

Project memory for Claude Code. Keep this file short; link to docs, don't copy them.

## What this is
SkillMatch is a resume screening and skill-matching tool for students (CSE-HackSpark-2026, Stage 1, Theme 3: AI for Everyday Life).
Upload a resume (PDF/DOCX), paste or pick a job description, get a match score, matched skills, missing skills and an explanation.
Core theme across all 3 stages: **student employability and skill development**.

## Stack
Python 3.11 · Streamlit UI · pdfplumber / python-docx parsing · rapidfuzz + curated skill taxonomy (`data/skills.json`) · sentence-transformers (MiniLM) with TF-IDF fallback · pytest · ruff.
Everything runs locally and offline after setup. No resume data leaves the machine.

## Commands
- Setup: `bash scripts/setup.sh`
- Run app: `streamlit run src/ui/app.py`
- Tests: `pytest -q`
- Lint/format: `ruff check . --fix && ruff format .`

## Conventions
- Type hints on all public functions; small pure functions; one responsibility per module.
- Layers: `parsing` (file -> text) -> `extraction` (text -> skills) -> `matching` (skills + text -> score) -> `ui`. UI never contains logic.
- Data contracts live in `src/matching/models.py` (dataclasses). Don't pass raw dicts between layers.
- Errors: raise typed exceptions from `src/utils/errors.py`; the UI turns them into friendly messages.

## Testing
- Every module in `parsing/`, `extraction/`, `matching/` needs unit tests in `tests/`.
- Sample resumes go in `data/samples/` (synthetic or consented only, never real personal data in git).

## Git
- Branch per ticket: `feat/T-05-skill-extractor`. Small commits, imperative messages.
- Never commit `.env`, `data/samples/*` with real PII, or model caches.

## Security (full rules in docs/security.md)
- Validate every upload (type, size, magic bytes). Never use `eval`/`exec`/`pickle` on user input.
- Never render user text with `unsafe_allow_html=True`.
- Don't log resume text or contact details.

## Scope guard (important)
Stage 1 has ~7 hours (9:30 AM - 4:30 PM). Build only what `docs/prd.md` marks **Must** or **Should**.
Stage 2/3 ideas live in `docs/roadmap.md`. Do not build them now.

## Docs index
docs/prd.md · docs/trd.md · docs/design.md · docs/security.md · docs/architecture.md · docs/problem-definition.md · docs/testing.md · docs/tickets.md · docs/demo-script.md · docs/roadmap.md · docs/onboarding.md
