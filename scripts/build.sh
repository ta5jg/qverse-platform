#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[BUILD] Running Python compile validation..."
python3 -m compileall api scripts agent ai ecosystem game infrastructure installer

echo "[BUILD] Running project audit..."
python3 scripts/audit_project.py
python3 scripts/repair_project.py --json

echo "[BUILD] Validating Docker Compose..."
docker compose -f deploy/docker/docker-compose.yml config

echo "[BUILD] Building Q-Verse API image..."
docker build -t qverse-api:latest .

echo "[BUILD] Build complete."
