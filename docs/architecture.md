# Architecture — SkillMatch

## Layers
```
            +--------------------+
            |  ui (Streamlit)    |  rendering only
            +---------+----------+
                      |
            +---------v----------+
            |  pipeline          |  request orchestration
            +---------+----------+
                      |
            +---------v----------+
            |  matching          |  scorer, similarity, models
            +---------+----------+
                      |
            +---------v----------+
            |  extraction        |  taxonomy, extractor, jd_parser
            +---------+----------+
                      |
            +---------v----------+
            |  parsing           |  validators, pdf/docx -> text
            +--------------------+
   utils: errors, text cleaning, logging (used by all layers)
   data:  skills.json (taxonomy), roles/ (preset JDs), samples/ (gitignored)
```
Dependencies point downward only. `ui` delegates each analysis to `src/pipeline.py`;
the pipeline coordinates parsing, extraction, and matching. Lower layers never
import `ui`.

## Folder layout
```
skillmatch/
├── CLAUDE.md
├── README.md
├── .claude/ (settings.json, commands/, skills/, agents/)
├── docs/
├── src/ { pipeline.py, parsing/, extraction/, matching/, ui/, utils/ }
├── tests/
├── data/ { skills.json, roles/, samples/ }
├── scripts/ { setup.sh, run.sh }
├── requirements.txt
└── .env.example
```

## Key decisions
| Decision | Why |
|---|---|
| Taxonomy-based extraction instead of an LLM | Fast, free, offline, explainable, deterministic |
| Embeddings with TF-IDF fallback | Semantic wins on stage; fallback protects the demo |
| No database | Nothing to persist in Stage 1; less to break and less PII risk |
| Dataclass contracts between layers | Easy testing and clear boundaries |
| Streamlit | Fastest route to a working UI within the time limit |

## Extension points (Stage 2/3)
- `extraction`: add a role-requirements table -> skill-gap ranking.
- `matching`: add learner-profile scoring.
- New `learning/` layer: paths + quizzes (Stage 2).
- New `guidance/` layer: RAG + LLM (Stage 3).
