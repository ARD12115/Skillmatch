#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n .env.example .env || true
# Pre-download the embedding model now (needs internet once), so the demo works offline.
python - <<'PY'
from sentence_transformers import SentenceTransformer
SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Embedding model cached.")
PY
echo "Setup done. Run: streamlit run src/ui/app.py"
