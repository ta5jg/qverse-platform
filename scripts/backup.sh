#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${QVERSE_BACKUP_DIR:-backups}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "[BACKUP] Creating Q-Verse database backup..."
docker exec qverse-postgres pg_dump -U qverse qverse > "$BACKUP_DIR/qverse_${TIMESTAMP}.sql"

echo "[BACKUP] Backup written to $BACKUP_DIR/qverse_${TIMESTAMP}.sql"
