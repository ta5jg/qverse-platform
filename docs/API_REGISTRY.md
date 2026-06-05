
# Q-Verse API Registry

## Purpose

This document defines the official API contract for the Q-Verse Platform.

The API Gateway is the single entry point for:

- Admin Panel
- Agents
- Integrations
- External Applications
- SDKs
- Future Mobile Applications

---

## API Principles

### Base URL

```text
https://agents.q-verse.io
```

### API Version

```text
/v1
```

### Authentication

All protected endpoints require:

```http
Authorization: Bearer <API_KEY>
```

Optional:

```http
X-User-Id: <USER_ID>
```

---

## Models API

### List Models

```http
GET /v1/models
```

Response:

```json
{
  "object": "list",
  "data": [
    {
      "id": "qverse-gemini",
      "object": "model"
    }
  ]
}
```

---

### Active Model

```http
GET /v1/admin/model
```

Returns currently selected model provider.

---

### Change Active Model

```http
POST /v1/admin/model
```

Request:

```json
{
  "provider": "gemini"
}
```

Supported providers:

- gemini
- openai
- anthropic
- deepseek
- openrouter
- ollama
- lmstudio

---

## Chat API

### Chat Completion

```http
POST /v1/chat/completions
```

OpenAI-compatible endpoint.

Request:

```json
{
  "model": "qverse-gemini",
  "messages": [
    {
      "role": "user",
      "content": "Merhaba"
    }
  ]
}
```

---

## Projects API

### List Projects

```http
GET /v1/projects
```

Response:

```json
{
  "projects": []
}
```

---

### Project Details

```http
GET /v1/projects/:project
```

---

### Project Health

```http
GET /v1/projects/:project/health
```

---

### Project Deploy

```http
POST /v1/projects/:project/deploy
```

---

## Memory API

### Profiles

```http
GET /v1/admin/memory/profiles
```

---

### Conversations

```http
GET /v1/admin/memory/conversations
```

---

### Search Memory

```http
POST /v1/memory/search
```

---

## Agents API

### List Agents

```http
GET /v1/agents
```

---

### Agent Status

```http
GET /v1/agents/:agent
```

---

### Run Agent

```http
POST /v1/agents/:agent/run
```

---

## Tools API

### System Tool

```http
POST /v1/tools/system
```

Request:

```json
{
  "command": "uptime"
}
```

Supported commands:

- uptime
- disk
- memory
- docker_ps
- services

---

### File Tool

```http
POST /v1/tools/files
```

---

### Git Tool

```http
POST /v1/tools/git
```

---

### Docker Tool

```http
POST /v1/tools/docker
```

---

## Integrations API

### List Integrations

```http
GET /v1/integrations
```

---

### Telegram Configuration

```http
GET /v1/integrations/telegram
```

```http
POST /v1/integrations/telegram
```

---

### Discord Configuration

```http
GET /v1/integrations/discord
```

```http
POST /v1/integrations/discord
```

---

## Monitoring API

### System Status

```http
GET /v1/admin/status
```

Returns:

- API Status
- Docker Status
- PostgreSQL Status
- Redis Status
- Nginx Status
- n8n Status

---

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Installer API

### Audit System

```http
POST /v1/installer/audit
```

---

### Upgrade System

```http
POST /v1/installer/upgrade
```

---

### Repair System

```http
POST /v1/installer/repair
```

---

### Backup System

```http
POST /v1/installer/backup
```

---

## Future APIs

Planned:

- Marketplace API
- Billing API
- Usage API
- Notification API
- RAG API
- Vector Search API
- Multi-Node API
- Cluster Management API

---

## API Lifecycle

Endpoint states:

- planned
- development
- testing
- stable
- deprecated

Only stable endpoints are guaranteed for production use.
