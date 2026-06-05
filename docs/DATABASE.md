
# Q-Verse Database Architecture

## Purpose

The Database Layer is the persistence foundation of the Q-Verse Platform.

It stores:

- Users
- Agents
- Projects
- Conversations
- Memory
- Integrations
- Settings
- Audit Logs
- System Metadata

The database layer must support reliability, scalability, recoverability, and security.

---

## Database Strategy

Q-Verse uses a multi-layer storage architecture.

```text
Application Layer
        │
        ▼
PostgreSQL
        │
        ▼
Redis Cache
        │
        ▼
Backups
```

Primary storage:

- PostgreSQL

Caching:

- Redis

Future:

- Vector Database
- Object Storage

---

## PostgreSQL

PostgreSQL is the primary source of truth.

Responsibilities:

- User Data
- Agent Data
- Project Data
- Settings
- Audit Records
- Conversation Metadata

Requirements:

- ACID compliance
- Backups
- Migrations
- Role-based access

---

## Redis

Redis provides:

- Session Storage
- API Caching
- Queue Support
- Rate Limiting
- Temporary Context

Redis is never the primary source of truth.

---

## Core Tables

### qverse_users

Stores platform users.

Fields:

```text
id
username
email
role
status
created_at
updated_at
```

---

### qverse_profiles

Stores user profile memory.

Fields:

```text
user_id
name
preferences
metadata
created_at
updated_at
```

---

### qverse_conversations

Stores conversation metadata.

Fields:

```text
id
user_id
title
summary
created_at
updated_at
```

---

### qverse_memory

Stores structured memory records.

Fields:

```text
id
scope
entity_id
content
metadata
created_at
```

Scopes:

- user
- project
- agent
- system

---

### qverse_projects

Stores project registry information.

Fields:

```text
id
name
path
status
git_url
created_at
updated_at
```

---

### qverse_agents

Stores agent definitions.

Fields:

```text
id
name
version
status
permissions
model_preferences
created_at
```

---

### qverse_models

Stores model configuration.

Fields:

```text
id
provider
model_name
status
cost_profile
created_at
```

---

### qverse_integrations

Stores integration settings.

Fields:

```text
id
type
status
configuration
created_at
updated_at
```

---

### qverse_settings

Stores platform configuration.

Fields:

```text
key
value
updated_at
```

---

### qverse_audit_logs

Stores security and activity records.

Fields:

```text
id
user_id
agent_id
action
target
result
created_at
```

---

## Memory Architecture

Memory is divided into scopes.

```text
Global Memory
 ├─ System Memory
 ├─ Agent Memory
 ├─ Project Memory
 └─ User Memory
```

The Agent Orchestrator controls access.

---

## Database Migrations

All schema changes must use migrations.

Rules:

- Versioned
- Reversible
- Logged
- Tested

Migration files:

```text
installer/database/migrations.py
```

---

## Backup Strategy

Backups include:

- PostgreSQL Dumps
- Redis Snapshots
- Configuration Data

Backup types:

```text
Daily
Weekly
Monthly
Manual
```

---

## Security Requirements

Requirements:

- Authenticated access
- Encrypted credentials
- Least privilege roles
- Audit logging
- Backup verification

Frontend applications never access databases directly.

---

## Monitoring

Tracked metrics:

- Connection Count
- Query Performance
- Database Size
- Cache Hit Rate
- Replication Status
- Backup Status

---

## Future Extensions

- pgvector
- Dedicated Vector Database
- Multi-region Replication
- Data Retention Policies
- Knowledge Graph Layer
- Distributed Storage

---

## Golden Rule

PostgreSQL is the source of truth.

Redis accelerates access.

Agents and applications must access data through approved services, never through direct uncontrolled database access.
