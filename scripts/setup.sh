#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR${PYTHONPATH:+:$PYTHONPATH}"

python3 -m venv "$VENV_DIR"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "$ROOT_DIR/requirements.txt"
cp -n "$ROOT_DIR/.env.example" "$ROOT_DIR/.env" || true

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

echo "Setup done. Run from the repo root: bash scripts/run.sh"
