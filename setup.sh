#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

python3 -m venv .venv
"$PROJECT_DIR/.venv/bin/python" -m pip install --upgrade pip
"$PROJECT_DIR/.venv/bin/pip" install -r requirements.txt
"$PROJECT_DIR/.venv/bin/python" -m pytest -q

echo "Entorno preparado. Ejecuta: source .venv/bin/activate && python run_pipeline.py"