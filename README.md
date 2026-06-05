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
