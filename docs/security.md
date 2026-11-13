# Security and Privacy — SkillMatch

Resumes contain personal data (name, phone, email, address). Treat them as sensitive even in a hackathon.

## 1. Principles
1. Local-only processing: no resume text sent to any third party in Stage 1.
2. Minimal retention: nothing stored unless the user downloads a report.
3. Least surprise: say clearly what the app does with files.

## 2. Threats and controls
| # | Threat | Control |
|---|---|---|
| 1 | Malicious upload (disguised file, huge file, PDF bombs) | Validate extension AND magic bytes (`%PDF`, `PK` for DOCX); `MAX_UPLOAD_MB` (default 5); page cap (e.g. 10 pages); parse inside try/except with a timeout where possible |
| 2 | XSS via resume text shown in UI | Render user text with `st.text`/`st.write`; never `unsafe_allow_html=True` with user content |
| 3 | Code injection | No `eval`, `exec`, `pickle.load` or shell calls on user-controlled data |
| 4 | PII leakage via logs | Log only events and counts (e.g. "parsed 2 pages, 14 skills"); never resume text, names, emails, phones |
| 5 | PII at rest | Don't write uploads to disk; if a temp file is unavoidable, delete it in a `finally` block |
| 6 | Secrets in repo | `.env` gitignored; Stage 1 needs no secrets; ship `.env.example` only |
| 7 | Supply chain | Install from PyPI only, from `requirements.txt`; pin versions once working (`pip freeze`) |
| 8 | Real resumes in git | `data/samples/*` is gitignored; use synthetic or consented resumes |
| 9 | Model download tampering | Use the official model name; cache it once; don't load models from unknown paths |
| 10 | Batch mode leaks between users | Session-scoped state only (`st.session_state`); clear on reset |

## 3. Responsible use and bias
- The score is **decision support**, not a hiring decision. State this in the UI.
- Match only on skills. Do not use or infer name, gender, age, college, photo or location.
- Strip or ignore contact details before similarity scoring.
- Document known limits: taxonomy coverage, non-English resumes, creative layouts.
- Show evidence and the formula so results can be challenged.

## 4. Pre-demo checklist
- [ ] `.env` and real resumes are not in git
- [ ] No `unsafe_allow_html` with user text (`grep -rn unsafe_allow_html src`)
- [ ] Upload validation tests pass
- [ ] Logs checked: no PII
- [ ] Demo uses synthetic or consented resumes only

## 5. Future (Stage 2/3)
Auth for multi-user use, encryption at rest if storing profiles, consent screen, data-retention policy, rate limiting if any LLM/API is added, audit of LLM prompts for PII.
