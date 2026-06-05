#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[DEV] Validating Q-Verse runtime..."
python3 -m py_compile api/main.py
python3 scripts/audit_project.py

echo "[DEV] Starting Q-Verse API on http://0.0.0.0:8000"
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
