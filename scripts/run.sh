#!/usr/bin/env bash
set -euo pipefail
if [ -x ".venv/bin/streamlit" ]; then
    source .venv/bin/activate
    exec streamlit run src/ui/app.py
elif [ -x ".venv/Scripts/streamlit.exe" ]; then
    exec .venv/Scripts/streamlit.exe run src/ui/app.py
else
    echo "Virtual environment not found. Run the setup instructions first." >&2
    exit 1
fi
