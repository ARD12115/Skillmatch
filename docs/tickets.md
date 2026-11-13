# Tickets — Stage 1 build plan

The event runs 9:30 AM - 4:30 PM (about 7 hours). If you start late, cut from the bottom (Could, then Should). Times are time-boxes, not promises.

| ID | Ticket | Priority | Est. | Done when |
|---|---|---|---|---|
| T-01 | Project setup: venv, requirements, run "hello" Streamlit page | Must | 15m | `bash scripts/run.sh` opens the app |
| T-02 | Skill taxonomy `data/skills.json` (~100 skills + aliases) | Must | 45m | Loads via `load_taxonomy` |
| T-03 | Upload validation + PDF text extraction | Must | 45m | Sample PDF -> text; bad files rejected |
| T-04 | Skill extractor with evidence snippets | Must | 60m | Tests pass for aliases and `C++` |
| T-05 | JD input: paste + 3 preset roles | Must | 30m | Required/preferred split works |
| T-06 | Scorer with documented formula | Must | 40m | Breakdown shown in UI |
| T-07 | Results UI: score, chips, explanation, evidence | Must | 60m | Matches design.md |
| T-08 | Error states + disclaimer | Must | 20m | Scanned PDF shows message |
| T-09 | Semantic similarity + TF-IDF fallback | Should | 45m | Works with `USE_EMBEDDINGS=false` |
| T-10 | Evaluation on ~20 resumes, results table | Should | 45m | Precision/recall recorded |
| T-11 | DOCX support | Should | 20m | DOCX parses |
| T-12 | Batch ranking + CSV export | Should | 40m | Table sorted by score |
| T-13 | "Add these skills to improve your score" hints | Could | 20m | Shows top-5 missing |
| T-14 | Slides/problem description + demo rehearsal x2 | Must | 45m | Timed under 5 minutes |

## Suggested split (3-4 people)
- Person A: T-03, T-08, T-11 (parsing, validation)
- Person B: T-02, T-04, T-05 (taxonomy, extraction)
- Person C: T-06, T-09 (scoring, similarity)
- Person D: T-07, T-12, then T-10 and T-14 (UI, evaluation, presentation)

## Cut line
If short on time: finish T-01 to T-08 + T-14. That is a complete, demo-able Stage 1.
