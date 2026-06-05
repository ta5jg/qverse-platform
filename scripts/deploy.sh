#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="${QVERSE_DEPLOY_HOST:-user@your-server}"
TARGET_DIR="${QVERSE_DEPLOY_DIR:-~/qverse-platform}"

echo "[DEPLOY] Preparing deployment to ${TARGET_HOST}:${TARGET_DIR}"
echo "[DEPLOY] Running local build validation..."
bash scripts/build.sh

echo "[DEPLOY] Syncing deployment command..."
ssh "$TARGET_HOST" "cd $TARGET_DIR && git pull && docker compose -f deploy/docker/docker-compose.yml up -d --build"

echo "[DEPLOY] Deployment complete."
