#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n .env.example .env || true
# Pre-download the embedding model now (needs internet once), so the demo works offline.
python - <<'PY'
try:
    from sentence_transformers import SentenceTransformer

    SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Embedding model cached.")
except Exception as exc:
    print(
        "Embedding model cache unavailable "
        f"({type(exc).__name__}); the app will use TF-IDF fallback."
    )
PY
echo "Setup done. Run: streamlit run src/ui/app.py"
