# Q-Verse Platform Architecture

## Vision

Q-Verse Platform is an AI Agent OS designed to manage models, agents, tools, projects, integrations, memory, deployments, and infrastructure from a single secure control center.

## Core Principle

Visible but simple. Hidden but powerful.

Users see:

- Admin Panel
- Telegram
- API
- IDE integrations

The hidden core manages:

- Model routing
- Agent orchestration
- Tool execution
- Memory
- Security
- Projects
- Integrations
- Backups
- Deployment

## Main Modules

### 0. Architecture Contract

Defines the common standard for all modules.

Every module must support:

```python
detect()
install()
update()
repair()
backup()
restore()
validate()
status()
admin_api()
```

### 1. Core Module

Responsible for:

- Config
- State
- Logger
- Audit
- Backup hooks
- Installer lifecycle

### 2. Database & Memory Module

Responsible for:

- PostgreSQL
- Redis
- User memory
- Conversation memory
- Project memory
- Agent memory
- Settings storage

### 3. API Gateway Module

Responsible for:

- OpenAI-compatible API
- Admin API
- Tool API
- Model API
- Agent API
- Integration API

### 4. Admin Panel Module

Responsible for:

- Dashboard
- Projects
- Memory
- Models
- Agents
- Tools
- Integrations
- Docker
- System
- Installer
- Settings

Frontend structure:

```text
src/
├── api/
├── components/
├── pages/
├── hooks/
├── context/
├── App.jsx
└── main.jsx
```

### 5. Model Router Module

Responsible for:

- Gemini
- OpenAI
- Anthropic
- DeepSeek
- OpenRouter
- Ollama
- LM Studio
- Custom OpenAI-compatible APIs

Models must be changeable from Admin Panel.

### 6. Agent Orchestrator Module

Responsible for:

- Q-Verse Core Agent
- Developer Agent
- DevOps Agent
- Security Agent
- Research Agent
- Marketing Agent
- Personal Assistant Agent

### 7. Tool Engine Module

Responsible for:

- Files
- Git
- Docker
- SSH
- Terminal
- Deploy
- Logs
- Backups

### 8. Project Manager Module

Responsible for:

- Project registry
- File browser
- Git status
- Git log
- Deploy actions
- Project health

### 9. Integration Hub Module

Responsible for:

- Telegram
- Signal
- Discord
- Slack
- WhatsApp
- Email
- Webhooks

### 10. Security Module

Responsible for:

- API keys
- Admin authentication
- Permissions
- Firewall
- Fail2Ban
- Rate limiting
- Secret protection

### 11. Backup & Restore Module

Responsible for:

- PostgreSQL backups
- Project backups
- Config backups
- Nginx backups
- Systemd backups
- Restore workflows
- Snapshot integration

### 12. Monitoring & Logs Module

Responsible for:

- API health
- Docker health
- PostgreSQL health
- Redis health
- n8n health
- System logs
- Agent logs

### 13. Deployment Module

Responsible for:

- Local deploy
- VPS deploy
- GitHub deploy
- Docker deploy
- Admin build
- Nginx reload

### 14. Installer / Upgrade Module

Responsible for:

- Fresh VPS install
- Existing system upgrade
- Missing component repair
- Idempotent execution
- Safe rollback

### 15. Knowledge Base / RAG Module

Responsible for:

- Documents
- Project docs
- Vector search
- Agent knowledge
- Long-term project memory

### 16. User & Permission Module

Responsible for:

- Admin users
- Roles
- Access levels
- API clients
- Audit trails

### 17. Billing / Usage / Quota Module

Responsible for:

- Model usage
- Token usage
- Provider cost
- Quotas
- Reports

### 18. Notification Module

Responsible for:

- Telegram alerts
- Email alerts
- System alerts
- Deployment alerts
- Backup alerts

### 19. Marketplace / Plugin Module

Responsible for:

- Installable tools
- Installable integrations
- Model plugins
- Agent templates

### 20. Local Runtime Module

Responsible for:

- Ollama
- LM Studio
- Local models
- Offline execution
- Local fallback

## Development Strategy

The full architecture is defined from the beginning.

Each module must become stable before being marked complete.

Module status levels:

```text
planned
scaffolded
development
testing
stable
deprecated
```

## Golden Rule

No module is considered complete unless it supports:

```text
Install
Detect
Update
Repair
Backup
Restore
Validate
Log
Admin API
Admin UI
```

## Human Documentation and Machine Registry

Q-Verse uses two complementary documentation layers:

### Human-readable documentation

Markdown files are written for humans and agents to understand the platform vision, architecture, rules, decisions, and roadmap.

### Machine-readable registry

YAML files are written for the Q-Verse Agent OS, installers, admin panel, model router, and automation systems.

Examples:

- `machine/architecture.yaml`
- `machine/modules.yaml`
- `machine/models.yaml`
- `machine/agents.yaml`
- `machine/tools.yaml`
- `machine/integrations.yaml`
- `machine/api.yaml`
- `machine/permissions.yaml`
- `machine/backend.yaml`
- `machine/database.yaml`
- `machine/deployment.yaml`
- `machine/frontend.yaml`
- `machine/installer.yaml`
- `machine/monitoring.yaml`
- `machine/notifications.yaml`
- `machine/project_status.yaml`
- `machine/repository.yaml`
- `machine/roadmap.yaml`
- `machine/services.yaml`
- `machine/module_contract.yaml`

Markdown explains why.

YAML defines what.

Code executes how.
