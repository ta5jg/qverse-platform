#!/usr/bin/env python3
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = {
    "README.md": """\
# Q-Verse

## Architecture Overview

- **Frontend:** User-facing web application built with modern JavaScript frameworks.
- **Backend:** FastAPI or Python-based API exposing core application logic.
- **Agent:** Autonomous AI agents handling advanced tasks and integrations.
- **AI:** Integration with OpenAI, Gemini, and custom models for intelligence.
- **Ecosystem:** Modular plugins, extensions, and external services.
- **Game:** Interactive, gamified experiences and simulations.
- **Infrastructure:** Cloud-native deployment, containerization, CI/CD, monitoring.

## Local Startup

1. Copy `.env.example` to `.env` and fill in secrets.
2. Run `docker compose -f deploy/docker/docker-compose.yml up -d`
3. Start the API: `bash scripts/dev.sh`
4. Access services at [http://localhost:8000](http://localhost:8000)

## Deployment

1. Build and tag images: `bash scripts/build.sh`
2. Deploy to server: `bash scripts/deploy.sh`
3. Systemd and Nginx configs are under `deploy/`
""",
    ".gitignore": """\
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
env/
.env
.venv/
build/
dist/
.eggs/
*.egg-info/

# Node/Vite
node_modules/
dist/
.vite/

# macOS
.DS_Store

# Logs
logs/
*.log

# Environment
.env
.env.*

# Misc
coverage/
*.sqlite3
""",
    ".env.example": """\
OPENAI_API_KEY=
GEMINI_API_KEY=
DATABASE_URL=
REDIS_URL=
JWT_SECRET=
""",
    "deploy/docker/docker-compose.yml": """\
version: '3.9'

services:
  postgres:
    image: postgres:15
    container_name: qverse-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: qverse
      POSTGRES_PASSWORD: qverse
      POSTGRES_DB: qverse
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U qverse"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    container_name: qverse-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  qverse-api:
    build:
      context: ../..
      dockerfile: Dockerfile
    container_name: qverse-api
    restart: unless-stopped
    command: bash scripts/dev.sh
    env_file:
      - ../../.env
    environment:
      DATABASE_URL: postgresql://qverse:qverse@postgres:5432/qverse
      REDIS_URL: redis://redis:6379/0
      QVERSE_ENV: production
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ../../:/app

  nginx:
    image: nginx:1.25-alpine
    container_name: qverse-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../nginx/agents.q-verse.io.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - qverse-api

volumes:
  postgres_data:
  redis_data:
""",
    "deploy/systemd/qverse-ai-api.service": """\
[Unit]
Description=Q-Verse AI API Service
After=network.target
Requires=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=%h/qverse-platform
ExecStart=/usr/bin/env bash scripts/dev.sh
Restart=on-failure
RestartSec=5
EnvironmentFile=%h/qverse-platform/.env

[Install]
WantedBy=multi-user.target
""",
    "deploy/nginx/agents.q-verse.io.conf": """\
server {
    listen 80;
    server_name agents.q-verse.io;

    client_max_body_size 50m;

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript application/xml;

    location / {
        proxy_pass http://qverse-api:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 300;
    }

    location /health {
        proxy_pass http://qverse-api:8000/health;
    }
}
""",
    ".github/workflows/ci.yml": """\
name: Q-Verse CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Python compile validation
        run: |
          python -m compileall api scripts agent ai ecosystem game infrastructure installer

      - name: Project audit
        run: |
          python scripts/audit_project.py
          python scripts/repair_project.py --json

      - name: Docker compose config validation
        run: |
          docker compose -f deploy/docker/docker-compose.yml config

      - name: Frontend package validation
        run: |
          cd frontend
          npm install --ignore-scripts
          npm run build --if-present
""",
    "machine/policies/development.yaml": """\
environment: development
logging:
  level: debug
security:
  require_https: false
  allow_localhost: true
runtime:
  reload: true
  workers: 1
backup:
  enabled: false
monitoring:
  enabled: true
agent:
  mode: local
ai:
  provider_mode: mock_or_local
""",
    "machine/policies/staging.yaml": """\
environment: staging
logging:
  level: info
security:
  require_https: true
  allow_localhost: false
runtime:
  reload: false
  workers: 2
backup:
  enabled: true
  retention_days: 7
monitoring:
  enabled: true
agent:
  mode: managed
ai:
  provider_mode: hybrid
""",
    "machine/policies/production.yaml": """\
environment: production
logging:
  level: warning
security:
  require_https: true
  allow_localhost: false
runtime:
  reload: false
  workers: 4
backup:
  enabled: true
  retention_days: 30
monitoring:
  enabled: true
agent:
  mode: enterprise
ai:
  provider_mode: managed
""",
    "scripts/dev.sh": """\
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[DEV] Validating Q-Verse runtime..."
python3 -m py_compile api/main.py
python3 scripts/audit_project.py

echo "[DEV] Starting Q-Verse API on http://0.0.0.0:8000"
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
""",
    "scripts/build.sh": """\
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
""",
    "scripts/deploy.sh": """\
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
""",
    "scripts/backup.sh": """\
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${QVERSE_BACKUP_DIR:-backups}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "[BACKUP] Creating Q-Verse database backup..."
docker exec qverse-postgres pg_dump -U qverse qverse > "$BACKUP_DIR/qverse_${TIMESTAMP}.sql"

echo "[BACKUP] Backup written to $BACKUP_DIR/qverse_${TIMESTAMP}.sql"
""",
    "Dockerfile": """\
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY . .

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "Makefile": """\
.PHONY: dev build audit repair compose-up compose-down backup

dev:
	bash scripts/dev.sh

build:
	bash scripts/build.sh

audit:
	python3 scripts/audit_project.py

repair:
	python3 scripts/repair_project.py --json

compose-up:
	docker compose -f deploy/docker/docker-compose.yml up -d --build

compose-down:
	docker compose -f deploy/docker/docker-compose.yml down

backup:
	bash scripts/backup.sh
""",
    "deploy/monitoring/prometheus.yml": """\
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: qverse-api
    static_configs:
      - targets: ['qverse-api:8000']
""",
}

def write_file(path, content, force=False):
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists() or force or file_path.read_text(encoding="utf-8").strip() == "":
        file_path.write_text(content, encoding="utf-8")
        print(f"[WRITE] {path}")
        return True
    else:
        print(f"[SKIP] {path}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Q-Verse V9 DevOps Bootstrap")
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    args = parser.parse_args()

    print("Q-Verse V9 DevOps Bootstrap Started")
    count = 0
    for rel_path, content in FILES.items():
        if write_file(rel_path, content, force=args.force):
            count += 1
    print(f"[SUMMARY] DevOps assets generated: {count}")
    print("[DEVOPS] Documentation, CI/CD, Docker, Nginx, Monitoring, Policies, Scripts and Runtime ready")
    print("Q-Verse V9 DevOps Bootstrap Complete")

if __name__ == "__main__":
    main()