# Onboarding — SkillMatch

## Setup (10 minutes, needs internet once)
```bash
git clone <repo-url> && cd skillmatch
bash scripts/setup.sh        # venv, deps, caches embedding model
bash scripts/run.sh
```
Windows: create the venv and install `requirements.txt` in PowerShell, then run
`bash scripts/run.sh` from Git Bash or WSL.

## Using Claude Code (optional)
```bash
npm i -g @anthropic-ai/claude-code
cd skillmatch && claude
```
Useful: `/review`, `/test-all`, `/bootstrap parsing/pdf_parser`, `/demo-check`.
Subagents: `code-reviewer`, `test-writer`, `security-auditor`. Read `CLAUDE.md` first.

## Workflow
1. Pick a ticket from `docs/tickets.md`.
2. Branch: `feat/T-04-skill-extractor`.
3. Build + tests, run `ruff check .`, `ruff format --check .`, and `pytest -q`.
4. Commit, merge, tell the team.

## Rules of the road
- Follow `docs/security.md`. No real resumes in git.
- Don't build Stage 2/3 features now.
- If a requirement is unclear, `docs/prd.md` wins; if technical, `docs/trd.md` wins.
