# SkillMatch

Resume screening and skill matching for students. Built for CSE-HackSpark-2026 (Canara Engineering College).

> Upload a resume, pick a target role, see your match score, the skills you have, the skills you're missing, and why.

## Quick start
```bash
bash scripts/setup.sh
bash scripts/run.sh
```

On Windows, create the environment and install dependencies in PowerShell, then
run the app from Git Bash or WSL with the repository runner:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
```bash
bash scripts/run.sh
```
To preload semantic embeddings on Windows when internet is available, run:
```powershell
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```
Copy `.env.example` to `.env` to adjust supported local settings such as the upload
limit (the server enforces a 5 MB maximum).

The app supports PDF and DOCX resumes, preset roles or a pasted job description,
explainable single-resume results, and batch ranking with CSV download. If the
embedding model is unavailable, text similarity falls back to local TF-IDF.

## Docs
See `docs/` — start with `prd.md`, then `trd.md`. Claude Code config is in `.claude/`.

## Team
<Team name> — <leader>, <members> · Mentor: <faculty guide>
