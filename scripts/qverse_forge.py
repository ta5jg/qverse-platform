#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "QVERSE_FORGE_V1"

REQUIRED_DIRS = [
    "agent/registry", "agent/supervisor", "agent/workers", "agent/scheduler",
    "agent/coordination", "agent/events", "agent/workflows", "agent/plugins",
    "memory/core", "memory/storage", "memory/vector", "memory/project",
    "ai/providers", "ai/router", "ai/response", "ai/monitoring", "ai/cost",
    "integrations/github", "integrations/telegram", "integrations/twitter",
    "clients/vscode", "clients/cursor", "clients/mcp",
    "frontend/admin/pages", "frontend/admin/components",
    "api/routes", "api/managers", "security", "audit", "reports"
]

FILES = {
    "agent/events/EventBus.py": '''
class EventBus:
    def __init__(self):
        self.events = []

    def publish(self, topic, payload=None):
        event = {"id": len(self.events) + 1, "topic": topic, "payload": payload or {}}
        self.events.append(event)
        return event

    def list_events(self):
        return self.events

event_bus = EventBus()
''',

    "agent/scheduler/TaskQueue.py": '''
class TaskQueue:
    def __init__(self):
        self.tasks = []

    def add(self, title, payload=None):
        task = {"id": len(self.tasks) + 1, "title": title, "payload": payload or {}, "status": "queued"}
        self.tasks.append(task)
        return task

    def next(self):
        for task in self.tasks:
            if task["status"] == "queued":
                task["status"] = "running"
                return task
        return None

    def list(self):
        return self.tasks

task_queue = TaskQueue()
''',

    "agent/registry/AgentRegistry.py": '''
class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, name, config=None):
        self.agents[name] = config or {"status": "active"}
        return {"registered": name, "config": self.agents[name]}

    def list_agents(self):
        return self.agents

agent_registry = AgentRegistry()
''',

    "agent/registry/ProjectRegistry.py": '''
class ProjectRegistry:
    def __init__(self):
        self.projects = {}

    def add_project(self, name, config=None):
        self.projects[name] = config or {"status": "active"}
        return {"project": name, "config": self.projects[name]}

    def list_projects(self):
        return self.projects

project_registry = ProjectRegistry()
''',

    "agent/plugins/PluginRegistry.py": '''
class PluginRegistry:
    def __init__(self):
        self.plugins = {}

    def add_plugin(self, name, config=None):
        self.plugins[name] = config or {"enabled": True}
        return {"plugin": name, "config": self.plugins[name]}

    def list_plugins(self):
        return self.plugins

plugin_registry = PluginRegistry()
''',

    "agent/workflows/WorkflowEngine.py": '''
class WorkflowEngine:
    def __init__(self):
        self.workflows = {}

    def create(self, name, steps=None):
        self.workflows[name] = {"steps": steps or [], "status": "ready"}
        return self.workflows[name]

    def run(self, name, payload=None):
        workflow = self.workflows.get(name)
        if not workflow:
            return {"success": False, "error": "workflow_not_found"}
        return {"success": True, "workflow": name, "payload": payload or {}, "steps": workflow["steps"]}

workflow_engine = WorkflowEngine()
''',

    "memory/storage/PersistentMemory.py": '''
import json
from pathlib import Path

class PersistentMemory:
    def __init__(self, path="data/qverse_memory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def load(self):
        return json.loads(self.path.read_text(encoding="utf-8") or "{}")

    def save(self, namespace, key, value):
        data = self.load()
        data.setdefault(namespace, {})[key] = value
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"status": "ok", "namespace": namespace, "key": key}

    def get(self, namespace, key):
        return self.load().get(namespace, {}).get(key)

persistent_memory = PersistentMemory()
''',

    "memory/vector/VectorMemory.py": '''class VectorMemory:
    def __init__(self):
        self.records = list()

    def add(self, text, metadata=None):
        item = {"id": len(self.records) + 1, "text": text, "metadata": metadata or {}}
        self.records.append(item)
        return item

    def search(self, query, limit=5):
        hits = [item for item in self.records if query.lower() in item["text"].lower()]
        return hits[:limit]

vector_memory = VectorMemory()
''',

    "memory/storage/SecretStore.py": '''import json
from pathlib import Path


class SecretStore:
    def __init__(self, path="data/qverse_secrets.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def load(self):
        return json.loads(self.path.read_text(encoding="utf-8") or "{}")

    def save_secret(self, name, value):
        data = self.load()
        data[name] = value
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"name": name, "configured": bool(value), "masked": self.mask(value)}

    def get_secret(self, name):
        return self.load().get(name)

    def list_secrets(self):
        data = self.load()
        return {name: {"configured": bool(value), "masked": self.mask(value)} for name, value in data.items()}

    def mask(self, value):
        if not value:
            return ""
        if len(value) <= 8:
            return "****"
        return value[:4] + "..." + value[-4:]


secret_store = SecretStore()
''',

    "ai/cost/ProviderCostRouter.py": '''
class ProviderCostRouter:
    COST_ORDER = ["deepseek", "qwen", "gemini", "openai", "claude"]

    def select_for_budget(self, available):
        for provider in self.COST_ORDER:
            if provider in available:
                return provider
        return available[0] if available else None

provider_cost_router = ProviderCostRouter()
''',

    "ai/monitoring/ProviderHealthCache.py": '''
import os

class ProviderHealthCache:
    KEYS = {
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "QWEN_API_KEY",
    }

    def status(self):
        return {
            provider: {"configured": bool(os.getenv(env_key))}
            for provider, env_key in self.KEYS.items()
        }

provider_health_cache = ProviderHealthCache()
''',

    "ai/monitoring/ProviderHealthMonitor.py": '''import os


class ProviderHealthMonitor:
    KEYS = {
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "QWEN_API_KEY",
    }

    def build_status(self):
        providers = {
            provider: {"configured": bool(os.getenv(env_key)), "env_key": env_key}
            for provider, env_key in self.KEYS.items()
        }
        configured_count = sum(1 for item in providers.values() if item["configured"])
        return {
            "providers": providers,
            "configured_count": configured_count,
            "healthy": configured_count > 0,
        }


provider_health_monitor = ProviderHealthMonitor()
''',

    "ai/providers/ProviderAdmin.py": '''import os
from memory.storage.SecretStore import secret_store


class ProviderAdmin:
    PROVIDER_KEYS = {
        "openai": "OPENAI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "QWEN_API_KEY",
    }

    def save_provider_key(self, provider, api_key):
        env_key = self.PROVIDER_KEYS.get(provider)
        if not env_key:
            return {"success": False, "error": "unsupported_provider", "provider": provider}
        saved = secret_store.save_secret(env_key, api_key)
        return {"success": True, "provider": provider, "env_key": env_key, "secret": saved}

    def list_providers(self):
        secrets = secret_store.list_secrets()
        providers = {}
        for provider, env_key in self.PROVIDER_KEYS.items():
            stored = secrets.get(env_key, {})
            providers[provider] = {
                "env_key": env_key,
                "configured": bool(os.getenv(env_key)) or stored.get("configured", False),
                "masked": stored.get("masked", ""),
            }
        return providers


provider_admin = ProviderAdmin()
''',

    "security/PermissionLayer.py": '''
class PermissionLayer:
    def __init__(self):
        self.roles = {
            "admin": ["*"],
            "developer": ["agent:run", "project:read", "project:write"],
            "viewer": ["project:read"],
        }

    def can(self, role, permission):
        allowed = self.roles.get(role, [])
        return "*" in allowed or permission in allowed

permission_layer = PermissionLayer()
''',

    "audit/AuditLogger.py": '''
import json
from datetime import datetime, timezone
from pathlib import Path

class AuditLogger:
    def __init__(self, path="reports/audit_log.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event, payload=None):
        record = {
            "event": event,
            "payload": payload or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\\n")
        return record

audit_logger = AuditLogger()
''',

    "integrations/twitter/TwitterRuntime.py": '''
class TwitterRuntime:
    def __init__(self):
        self.safe_mode = True
        self.drafts = []

    def draft_post(self, text):
        draft = {"id": len(self.drafts) + 1, "text": text, "status": "draft", "safe_mode": self.safe_mode}
        self.drafts.append(draft)
        return draft

    def list_drafts(self):
        return self.drafts

twitter_runtime = TwitterRuntime()
''',

    "integrations/github/GitHubRuntime.py": '''
class GitHubRuntime:
    def handle_webhook(self, event, payload=None):
        return {"integration": "github", "event": event, "payload": payload or {}, "status": "received"}

github_runtime = GitHubRuntime()
''',

    "integrations/telegram/TelegramRuntime.py": '''
class TelegramRuntime:
    def handle_message(self, message):
        return {"integration": "telegram", "message": message, "status": "received"}

telegram_runtime = TelegramRuntime()
''',

    "api/routes/__init__.py": '''"""
Q-Verse API Routes Registry V12 Forge Hardened
"""

from dataclasses import dataclass
from typing import List

from fastapi import APIRouter

from api.routes.admin import router as admin_router
from api.routes.agents import router as agents_router
from api.routes.audit import router as audit_router
from api.routes.backup import router as backup_router
from api.routes.config import router as config_router
from api.routes.database import router as database_router
from api.routes.deployments import router as deployments_router
from api.routes.engines import router as engines_router
from api.routes.forge import router as forge_router
from api.routes.health import router as health_router
from api.routes.integrations import router as integrations_router
from api.routes.logs import router as logs_router
from api.routes.marketplace import router as marketplace_router
from api.routes.models import router as models_router
from api.routes.notifications import router as notifications_router
from api.routes.orchestrator import router as orchestrator_router
from api.routes.projects import router as projects_router
from api.routes.runtime import router as runtime_router
from api.routes.security import router as security_router
from api.routes.services import router as services_router
from api.routes.state import router as state_router
from api.routes.system import router as system_router
from api.routes.tasks import router as tasks_router
from api.routes.telemetry import router as telemetry_router
from api.routes.workflows import router as workflows_router
from api.routes.agent_chat import router as agent_chat_router

ROUTES_VERSION = "V12"
ROUTES_STATUS = "V12_FORGE_READY"


@dataclass(frozen=True)
class RouteDefinition:
    name: str
    prefix: str
    router: APIRouter
    version: str = ROUTES_VERSION
    enabled: bool = True


ROUTE_REGISTRY: List[RouteDefinition] = [
    RouteDefinition("forge", "/forge", forge_router),
    RouteDefinition("health", "/health", health_router),
    RouteDefinition("system", "/system", system_router),
    RouteDefinition("runtime", "/runtime", runtime_router),
    RouteDefinition("services", "/services", services_router),
    RouteDefinition("engines", "/engines", engines_router),
    RouteDefinition("admin", "/admin", admin_router),
    RouteDefinition("telemetry", "/telemetry", telemetry_router),
    RouteDefinition("config", "/config", config_router),
    RouteDefinition("audit", "/audit", audit_router),
    RouteDefinition("backup", "/backup", backup_router),
    RouteDefinition("logs", "/logs", logs_router),
    RouteDefinition("state", "/state", state_router),
    RouteDefinition("projects", "/projects", projects_router),
    RouteDefinition("models", "/models", models_router),
    RouteDefinition("integrations", "/integrations", integrations_router),
    RouteDefinition("database", "/database", database_router),
    RouteDefinition("security", "/security", security_router),
    RouteDefinition("tasks", "/tasks", tasks_router),
    RouteDefinition("notifications", "/notifications", notifications_router),
    RouteDefinition("agents", "/agents", agents_router),
    RouteDefinition("agent_chat", "/agents", agent_chat_router),
    RouteDefinition("orchestrator", "/orchestrator", orchestrator_router),
    RouteDefinition("deployments", "/deployments", deployments_router),
    RouteDefinition("workflows", "/workflows", workflows_router),
    RouteDefinition("marketplace", "/marketplace", marketplace_router),
]


def enabled_routers() -> List[APIRouter]:
    return [route.router for route in ROUTE_REGISTRY if route.enabled]


def route_manifest() -> dict:
    enabled_routes = [route for route in ROUTE_REGISTRY if route.enabled]
    return {
        "version": ROUTES_VERSION,
        "status": ROUTES_STATUS,
        "total": len(ROUTE_REGISTRY),
        "enabled": len(enabled_routes),
        "routes": [
            {
                "name": route.name,
                "prefix": route.prefix,
                "version": route.version,
                "enabled": route.enabled,
            }
            for route in ROUTE_REGISTRY
        ],
    }
''',

    "api/routes/forge.py": '''
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any, Dict

from agent.events.EventBus import event_bus
from agent.scheduler.TaskQueue import task_queue
from agent.registry.AgentRegistry import agent_registry
from agent.registry.ProjectRegistry import project_registry
from agent.plugins.PluginRegistry import plugin_registry
from agent.workflows.WorkflowEngine import workflow_engine
from memory.storage.PersistentMemory import persistent_memory
from memory.vector.VectorMemory import vector_memory
from ai.monitoring.ProviderHealthCache import provider_health_cache
from ai.providers.ProviderAdmin import provider_admin
from integrations.twitter.TwitterRuntime import twitter_runtime
from integrations.github.GitHubRuntime import github_runtime
from integrations.telegram.TelegramRuntime import telegram_runtime
from security.PermissionLayer import permission_layer
from audit.AuditLogger import audit_logger

router = APIRouter(prefix="/forge", tags=["qverse-forge"])

class KeyValueRequest(BaseModel):
    namespace: str = "default"
    key: str
    value: Any

class TextRequest(BaseModel):
    text: str

class ProjectRequest(BaseModel):
    name: str
    config: Dict[str, Any] = Field(default_factory=dict)

class ProviderKeyRequest(BaseModel):
    provider: str
    api_key: str

@router.get("/status")
def status():
    return {
        "status": "ready",
        "providers": provider_health_cache.status(),
        "provider_admin": provider_admin.list_providers(),
        "tasks": task_queue.list(),
        "events": event_bus.list_events(),
        "agents": agent_registry.list_agents(),
        "projects": project_registry.list_projects(),
        "plugins": plugin_registry.list_plugins(),
    }

@router.get("/providers")
def list_providers():
    return provider_admin.list_providers()

@router.post("/providers/key")
def save_provider_key(req: ProviderKeyRequest):
    return provider_admin.save_provider_key(req.provider, req.api_key)

@router.post("/memory/save")
def memory_save(req: KeyValueRequest):
    return persistent_memory.save(req.namespace, req.key, req.value)

@router.get("/memory/{namespace}/{key}")
def memory_get(namespace: str, key: str):
    return {"namespace": namespace, "key": key, "value": persistent_memory.get(namespace, key)}

@router.post("/vector/add")
def vector_add(req: TextRequest):
    return vector_memory.add(req.text)

@router.get("/vector/search")
def vector_search(q: str):
    return {"results": vector_memory.search(q)}

@router.post("/tasks")
def add_task(req: ProjectRequest):
    return task_queue.add(req.name, req.config)

@router.post("/projects")
def add_project(req: ProjectRequest):
    return project_registry.add_project(req.name, req.config)

@router.post("/agents")
def add_agent(req: ProjectRequest):
    return agent_registry.register(req.name, req.config)

@router.post("/plugins")
def add_plugin(req: ProjectRequest):
    return plugin_registry.add_plugin(req.name, req.config)

@router.post("/twitter/draft")
def twitter_draft(req: TextRequest):
    return twitter_runtime.draft_post(req.text)

@router.post("/telegram/message")
def telegram_message(payload: Dict[str, Any]):
    return telegram_runtime.handle_message(payload)

@router.post("/github/webhook/{event}")
def github_webhook(event: str, payload: Dict[str, Any]):
    return github_runtime.handle_webhook(event, payload)

@router.get("/permission/check")
def permission_check(role: str, permission: str):
    return {"allowed": permission_layer.can(role, permission)}

@router.post("/audit/{event}")
def audit(event: str, payload: Dict[str, Any]):
    return audit_logger.log(event, payload)
''',

    "frontend/admin/pages/ForgeAdmin.jsx": '''import { useEffect, useState } from "react";

const API_BASE = "https://api.q-verse.io";

export default function ForgeAdmin() {
  const [status, setStatus] = useState(null);
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [projectName, setProjectName] = useState("");
  const [agentName, setAgentName] = useState("");
  const [message, setMessage] = useState("");

  async function refresh() {
    const res = await fetch(`${API_BASE}/forge/status`);
    setStatus(await res.json());
  }

  async function saveProviderKey() {
    const res = await fetch(`${API_BASE}/forge/providers/key`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider, api_key: apiKey })
    });
    const data = await res.json();
    setMessage(JSON.stringify(data, null, 2));
    setApiKey("");
    refresh();
  }

  async function addProject() {
    const res = await fetch(`${API_BASE}/forge/projects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: projectName, config: { source: "admin" } })
    });
    setMessage(JSON.stringify(await res.json(), null, 2));
    setProjectName("");
    refresh();
  }

  async function addAgent() {
    const res = await fetch(`${API_BASE}/forge/agents`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: agentName, config: { source: "admin" } })
    });
    setMessage(JSON.stringify(await res.json(), null, 2));
    setAgentName("");
    refresh();
  }

  useEffect(() => { refresh(); }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui", maxWidth: 1000 }}>
      <h1>Q-Verse Forge Admin</h1>
      <p>Manage providers, API keys, projects, agents, plugins, workflows, memory and integrations.</p>

      <section style={{ marginTop: 24 }}>
        <h2>Provider API Keys</h2>
        <select value={provider} onChange={(e) => setProvider(e.target.value)}>
          <option value="openai">OpenAI</option>
          <option value="claude">Claude</option>
          <option value="gemini">Gemini</option>
          <option value="deepseek">DeepSeek</option>
          <option value="qwen">Qwen</option>
        </select>
        <input
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter API key"
          type="text"
          style={{ marginLeft: 8, width: 360 }}
        />
        <button onClick={saveProviderKey} style={{ marginLeft: 8 }}>Save Key</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Projects</h2>
        <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project name" />
        <button onClick={addProject} style={{ marginLeft: 8 }}>Add Project</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Agents</h2>
        <input value={agentName} onChange={(e) => setAgentName(e.target.value)} placeholder="Agent name" />
        <button onClick={addAgent} style={{ marginLeft: 8 }}>Add Agent</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Live Forge Status</h2>
        <button onClick={refresh}>Refresh</button>
        <pre style={{ background: "#111", color: "#0f0", padding: 16, overflow: "auto" }}>
          {JSON.stringify(status, null, 2)}
        </pre>
      </section>

      {message && (
        <section style={{ marginTop: 24 }}>
          <h2>Last Action</h2>
          <pre style={{ background: "#f5f5f5", padding: 16 }}>{message}</pre>
        </section>
      )}
    </main>
  );
}
''',

# Add bootstrap runtime script before docs/QVERSE_FORGE.md
    "scripts/bootstrap_qverse_ultimate_v12_runtime.py": '''#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    print("Q-Verse V12 runtime bootstrap is delegated to scripts/qverse_forge.py")
    print(f"Project root: {ROOT}")


if __name__ == "__main__":
    main()
''',

    "docs/QVERSE_FORGE.md": '''
# Q-Verse Forge

Q-Verse Forge is the self-healing builder for the Q-Verse Agent Operating System.

It scans, repairs, upgrades, hardens and generates the platform layers:

- Agent Registry
- Project Registry
- Plugin System
- Workflow Engine
- Event Bus
- Task Queue
- Persistent Memory
- Vector Memory
- Provider Health Cache
- Permission Layer
- Audit Layer
- GitHub Runtime
- Telegram Runtime
- Twitter Safe Draft Runtime
- Admin Dashboard
'''
}


def write_file(path, content, force=False):
    target = ROOT / path
    if target.exists() and not force:
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")
    return True


def patch_routes_init():
    init_path = ROOT / "api/routes/__init__.py"
    if not init_path.exists():
        return {"patched": False, "reason": "api/routes/__init__.py not found"}

    text = init_path.read_text(encoding="utf-8")
    import_line = "from api.routes.forge import router as forge_router"
    if import_line not in text:
        lines = text.splitlines()
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("from api.routes"):
                insert_at = i + 1
        lines.insert(insert_at, import_line)
        text = "\\n".join(lines) + "\\n"

    if "enabled_routers = [" in text and "forge_router" not in text.split("enabled_routers = [", 1)[-1].split("]", 1)[0]:
        text = text.replace("enabled_routers = [", "enabled_routers = [\n    forge_router,")

    if "ROUTE_REGISTRY: List[RouteDefinition] = [" in text and 'RouteDefinition("forge", "/forge", forge_router)' not in text:
        text = text.replace(
            "ROUTE_REGISTRY: List[RouteDefinition] = [",
            "ROUTE_REGISTRY: List[RouteDefinition] = [\n    RouteDefinition(\"forge\", \"/forge\", forge_router),"
        )

    init_path.write_text(text, encoding="utf-8")
    return {"patched": True}


def scan_project():
    required = list(FILES.keys())
    missing = [p for p in required if not (ROOT / p).exists()]
    return {"required": len(required), "missing": missing, "missing_count": len(missing)}


def run_compile_checks():
    checks = [
        "api/routes/forge.py",
        "api/routes/__init__.py",
        "ai/monitoring/ProviderHealthMonitor.py",
        "ai/providers/ProviderAdmin.py",
        "memory/storage/SecretStore.py",
        "scripts/bootstrap_qverse_ultimate_v12_runtime.py",
        "agent/events/EventBus.py",
        "agent/scheduler/TaskQueue.py",
        "agent/registry/AgentRegistry.py",
        "agent/registry/ProjectRegistry.py",
        "agent/plugins/PluginRegistry.py",
        "agent/workflows/WorkflowEngine.py",
        "memory/storage/PersistentMemory.py",
        "memory/vector/VectorMemory.py",
        "security/PermissionLayer.py",
        "audit/AuditLogger.py",
        "integrations/twitter/TwitterRuntime.py",
        "integrations/github/GitHubRuntime.py",
        "integrations/telegram/TelegramRuntime.py",
    ]
    results = {}
    for item in checks:
        path = ROOT / item
        if not path.exists():
            results[item] = "missing"
            continue
        proc = subprocess.run(["python3", "-m", "py_compile", str(path)], capture_output=True, text=True)
        results[item] = "ok" if proc.returncode == 0 else proc.stderr
    return results


def write_report(written, skipped, scan_before, scan_after, route_patch, compile_results):
    report = {
        "version": VERSION,
        "status": "forge_complete",
        "route_registry_target": "ROUTE_REGISTRY",
        "self_healing": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "written_count": len(written),
        "skipped_count": len(skipped),
        "written": written,
        "skipped": skipped,
        "scan_before": scan_before,
        "scan_after": scan_after,
        "route_patch": route_patch,
        "compile": compile_results,
        "endpoints": [
            "/forge/status",
            "/forge/providers",
            "/forge/providers/key",
            "/forge/memory/save",
            "/forge/vector/add",
            "/forge/vector/search",
            "/forge/tasks",
            "/forge/projects",
            "/forge/agents",
            "/forge/plugins",
            "/forge/twitter/draft",
            "/forge/telegram/message",
            "/forge/github/webhook/{event}",
            "/forge/permission/check",
            "/forge/audit/{event}",
        ],
    }
    report_path = ROOT / "reports/qverse_forge_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="Q-Verse Forge - Self-Healing Platform Builder")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-patch-routes", action="store_true")
    args = parser.parse_args()

    print("Q-Verse Forge Started")

    scan_before = scan_project()
    written, skipped = [], []

    for path, content in FILES.items():
        if write_file(path, content, force=args.force):
            print(f"[WRITE] {path}")
            written.append(path)
        else:
            print(f"[SKIP] {path}")
            skipped.append(path)

    scan_after = scan_project()

    route_patch = {"patched": False, "reason": "disabled"}
    if not args.no_patch_routes:
        route_patch = patch_routes_init()
        print(f"[ROUTES] {route_patch}")

    compile_results = run_compile_checks()
    report_path = write_report(written, skipped, scan_before, scan_after, route_patch, compile_results)

    print(f"[SUMMARY] written={len(written)} skipped={len(skipped)}")
    print(f"[REPORT] {report_path.relative_to(ROOT)}")
    print("Q-Verse Forge Complete")


if __name__ == "__main__":
    main()