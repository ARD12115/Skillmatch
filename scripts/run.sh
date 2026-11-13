#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR${PYTHONPATH:+:$PYTHONPATH}"

if [ -x "$VENV_DIR/bin/streamlit" ]; then
    # shellcheck disable=SC1090
    source "$VENV_DIR/bin/activate"
    exec streamlit run "$ROOT_DIR/src/ui/app.py"
elif [ -x "$VENV_DIR/Scripts/streamlit.exe" ]; then
    exec "$VENV_DIR/Scripts/streamlit.exe" run "$ROOT_DIR/src/ui/app.py"
else
    echo "Virtual environment not found. Run the setup script from the repo root." >&2
    exit 1
fi
