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

    "ai/response/AIResponseEngine.py": '''import os
import requests

from memory.storage.SecretStore import secret_store


class AIResponseEngine:
    PROVIDER_ORDER = ["openai", "gemini", "deepseek", "qwen"]

    PROVIDER_KEYS = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "QWEN_API_KEY",
    }

    DEFAULT_MODELS = {
        "openai": "gpt-4o-mini",
        "gemini": "gemini-1.5-flash",
        "deepseek": "deepseek-chat",
        "qwen": "qwen-turbo",
    }

    def __init__(self):
        self.provider = os.getenv("QVERSE_DEFAULT_PROVIDER", "openai")
        self.model = os.getenv("OPENAI_MODEL", self.DEFAULT_MODELS["openai"])

    def _get_key(self, provider):
        env_key = self.PROVIDER_KEYS.get(provider)
        if not env_key:
            return None
        return os.getenv(env_key) or secret_store.get_secret(env_key)

    def _system_prompt(self, provider):
        return (
            "You are Q-Verse Agent, the live AI runtime of the Q-Verse Platform. "
            f"You are currently connected through the configured {provider} provider. "
            "When transport_enabled is true, you must answer as the live Q-Verse runtime. "
            "Do not claim you are offline, static, not connected, unable to answer live, or only a pre-trained assistant. "
            "If the user asks whether Q-Verse is connected to an AI provider, answer yes and explain briefly which configured provider produced the response. "
            "Answer in the user's language. Be concise, direct, and helpful."
        )

    def _provider_sequence(self, provider=None):
        requested = provider or self.provider or "openai"
        sequence = []
        if requested in self.PROVIDER_ORDER:
            sequence.append(requested)
        for item in self.PROVIDER_ORDER:
            if item not in sequence:
                sequence.append(item)
        return sequence

    def _model_for(self, provider, model=None):
        if model:
            return model
        if provider == "openai":
            return os.getenv("OPENAI_MODEL", self.DEFAULT_MODELS[provider])
        if provider == "gemini":
            return os.getenv("GEMINI_MODEL", self.DEFAULT_MODELS[provider])
        if provider == "deepseek":
            return os.getenv("DEEPSEEK_MODEL", self.DEFAULT_MODELS[provider])
        if provider == "qwen":
            return os.getenv("QWEN_MODEL", self.DEFAULT_MODELS[provider])
        return self.DEFAULT_MODELS.get(provider, self.model)

    def _chat_openai_compatible(self, provider, prompt, context=None, model=None):
        api_key = self._get_key(provider)
        if not api_key:
            raise RuntimeError(f"missing_api_key:{provider}")

        base_urls = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "deepseek": "https://api.deepseek.com/chat/completions",
            "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        }
        url = base_urls[provider]
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self._model_for(provider, model),
                "messages": [
                    {"role": "system", "content": self._system_prompt(provider)},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.4,
            },
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _chat_gemini(self, prompt, context=None, model=None):
        provider = "gemini"
        api_key = self._get_key(provider)
        if not api_key:
            raise RuntimeError("missing_api_key:gemini")

        gemini_model = self._model_for(provider, model)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={api_key}"
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": self._system_prompt(provider) + "\\n\\nUser: " + prompt}
                        ],
                    }
                ],
                "generationConfig": {"temperature": 0.4},
            },
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _try_provider(self, provider, prompt, context=None, model=None):
        if provider == "gemini":
            return self._chat_gemini(prompt, context=context, model=model)
        if provider in {"openai", "deepseek", "qwen"}:
            return self._chat_openai_compatible(provider, prompt, context=context, model=model)
        raise RuntimeError(f"unsupported_provider:{provider}")

    def respond(self, prompt, context=None, provider=None, model=None, **kwargs):
        attempts = []
        for candidate in self._provider_sequence(provider):
            try:
                text = self._try_provider(candidate, prompt, context=context, model=model)
                return {
                    "engine": "ai_response_engine",
                    "version": "V12.2",
                    "result": {
                        "provider": candidate,
                        "status": "completed",
                        "transport_enabled": True,
                        "prompt": prompt,
                        "context": context or {},
                        "response": text,
                        "fallback_used": candidate != (provider or self.provider or "openai"),
                        "attempts": attempts,
                    },
                }
            except Exception as exc:
                attempts.append({
                    "provider": candidate,
                    "error": exc.__class__.__name__,
                    "message": str(exc),
                })
                continue

        return {
            "engine": "ai_response_engine",
            "version": "V12.2",
            "result": {
                "provider": provider or self.provider or "openai",
                "status": "error",
                "transport_enabled": True,
                "prompt": prompt,
                "context": context or {},
                "response": None,
                "fallback_used": True,
                "attempts": attempts,
            },
        }

    def chat(self, prompt, context=None, provider=None, model=None, **kwargs):
        return self.respond(prompt, context=context, provider=provider, model=model, **kwargs)

    def generate(self, prompt, context=None, provider=None, model=None, **kwargs):
        return self.respond(prompt, context=context, provider=provider, model=model, **kwargs)


ai_response_engine = AIResponseEngine()
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


    "frontend/admin/components/SystemStatus.jsx": '''export default function SystemStatus({ status, onRefresh }) {
  const providers = status?.provider_admin || {};
  const projects = status?.projects || {};
  const agents = status?.agents || {};
  const plugins = status?.plugins || {};

  return (
    <section className="card system-card">
      <div className="card-header">
        <div>
          <p className="eyebrow">System</p>
          <h2>Runtime Status</h2>
        </div>
        <button className="btn ghost" onClick={onRefresh}>Refresh</button>
      </div>
      <div className="stats-grid compact">
        <div className="stat"><span>Providers</span><strong>{Object.keys(providers).length}</strong></div>
        <div className="stat"><span>Projects</span><strong>{Object.keys(projects).length}</strong></div>
        <div className="stat"><span>Agents</span><strong>{Object.keys(agents).length}</strong></div>
        <div className="stat"><span>Plugins</span><strong>{Object.keys(plugins).length}</strong></div>
      </div>
      <pre className="status-json">{JSON.stringify(status, null, 2)}</pre>
    </section>
  );
}
''',

    "frontend/admin/components/ProviderManager.jsx": '''const providerLabels = {
  openai: "OpenAI",
  claude: "Claude",
  gemini: "Gemini",
  deepseek: "DeepSeek",
  qwen: "Qwen",
};

export default function ProviderManager({ provider, setProvider, apiKey, setApiKey, onSave, providers = {} }) {
  const active = providers?.[provider];

  return (
    <section className="card accent-blue">
      <div className="card-header">
        <div>
          <p className="eyebrow">Providers</p>
          <h2>Provider API Keys</h2>
          <p className="muted">Manage live AI provider keys securely.</p>
        </div>
        <span className={active?.configured ? "pill ok" : "pill warn"}>{active?.configured ? "Configured" : "Missing"}</span>
      </div>
      <div className="form-row">
        <select value={provider} onChange={(e) => setProvider(e.target.value)}>
          {Object.entries(providerLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select>
        <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="Enter API key" type="password" />
        <button className="btn primary" onClick={onSave}>Save Key</button>
      </div>
      <p className="hint">Current key: {active?.masked || "not configured"}</p>
    </section>
  );
}
''',

    "frontend/admin/components/ProjectManager.jsx": '''export default function ProjectManager({ projectName, setProjectName, onAdd, projects = {} }) {
  return (
    <section className="card accent-green">
      <div className="card-header">
        <div>
          <p className="eyebrow">Core</p>
          <h2>Projects</h2>
          <p className="muted">Create and manage Q-Verse projects.</p>
        </div>
        <span className="pill ok">{Object.keys(projects).length} Active</span>
      </div>
      <div className="form-row">
        <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project name" />
        <button className="btn success" onClick={onAdd}>Add Project</button>
      </div>
      <ul className="mini-list">
        {Object.entries(projects).slice(0, 5).map(([name, cfg]) => <li key={name}><span>{name}</span><b>{cfg?.status || "active"}</b></li>)}
      </ul>
    </section>
  );
}
''',

    "frontend/admin/components/AgentManager.jsx": '''export default function AgentManager({ agentName, setAgentName, onAdd, agents = {} }) {
  return (
    <section className="card accent-purple">
      <div className="card-header">
        <div>
          <p className="eyebrow">Runtime</p>
          <h2>Agents</h2>
          <p className="muted">Create and manage AI agents.</p>
        </div>
        <span className="pill ok">{Object.keys(agents).length} Running</span>
      </div>
      <div className="form-row">
        <input value={agentName} onChange={(e) => setAgentName(e.target.value)} placeholder="Agent name" />
        <button className="btn purple" onClick={onAdd}>Add Agent</button>
      </div>
      <ul className="mini-list">
        {Object.entries(agents).slice(0, 5).map(([name, cfg]) => <li key={name}><span>{name}</span><b>{cfg?.status || "active"}</b></li>)}
      </ul>
    </section>
  );
}
''',

    "frontend/admin/components/PluginManager.jsx": '''export default function PluginManager({ pluginName, setPluginName, onAdd, plugins = {} }) {
  return (
    <section className="card accent-teal">
      <div className="card-header">
        <div>
          <p className="eyebrow">Extensions</p>
          <h2>Plugins</h2>
          <p className="muted">Install and manage integrations.</p>
        </div>
        <span className="pill ok">{Object.keys(plugins).length} Installed</span>
      </div>
      <div className="form-row">
        <input value={pluginName} onChange={(e) => setPluginName(e.target.value)} placeholder="Plugin name" />
        <button className="btn success" onClick={onAdd}>Add Plugin</button>
      </div>
      <ul className="mini-list">
        {Object.entries(plugins).slice(0, 5).map(([name, cfg]) => <li key={name}><span>{name}</span><b>{cfg?.enabled === false ? "disabled" : "enabled"}</b></li>)}
      </ul>
    </section>
  );
}
''',

    "frontend/admin/components/MemoryManager.jsx": '''export default function MemoryManager({ memoryKey, setMemoryKey, memoryValue, setMemoryValue, onSave }) {
  return (
    <section className="card">
      <div className="card-header">
        <div>
          <p className="eyebrow">Memory</p>
          <h2>Memory Manager</h2>
          <p className="muted">Save persistent memory values.</p>
        </div>
      </div>
      <div className="form-row">
        <input value={memoryKey} onChange={(e) => setMemoryKey(e.target.value)} placeholder="Memory key" />
        <input value={memoryValue} onChange={(e) => setMemoryValue(e.target.value)} placeholder="Memory value" />
        <button className="btn primary" onClick={onSave}>Save Memory</button>
      </div>
    </section>
  );
}
''',

    "frontend/admin/components/TwitterDraftManager.jsx": '''export default function TwitterDraftManager({ draftText, setDraftText, onDraft }) {
  return (
    <section className="card">
      <div className="card-header">
        <div>
          <p className="eyebrow">Integrations</p>
          <h2>Twitter/X Draft Queue</h2>
          <p className="muted">Create safe-mode social media drafts.</p>
        </div>
      </div>
      <textarea value={draftText} onChange={(e) => setDraftText(e.target.value)} placeholder="Draft safe-mode post" rows={4} />
      <button className="btn primary full" onClick={onDraft}>Create Draft</button>
    </section>
  );
}
''',
    "frontend/admin/components/LiveChatTest.jsx": '''export default function LiveChatTest({ chatMessage, setChatMessage, chatResult, onSend, loading }) {
  const aiResult = chatResult?.runtime?.ai_response?.result || chatResult?.ai_response?.result || {};
  const provider = aiResult?.provider;
  const fallback = aiResult?.fallback_used;
  const response = aiResult?.response || chatResult?.reply || "Henüz test yapılmadı.";

  return (
    <section className="card chat-card accent-purple" id="live-chat">
      <div className="card-header">
        <div>
          <p className="eyebrow">Live Runtime</p>
          <h2>Live Chat Test</h2>
          <p className="muted">Test the AI response engine in real time.</p>
        </div>
        <span className="pill purple">V12.2 Engine</span>
      </div>
      <div className="chat-window">
        <div className="bubble user">{chatMessage || "Bu cevabı hangi provider üretiyor?"}</div>
        <div className="bubble bot">{response}</div>
      </div>
      <div className="form-row chat-input-row">
        <input value={chatMessage} onChange={(e) => setChatMessage(e.target.value)} placeholder="Mesajınızı yazın..." />
        <button className="btn purple" onClick={onSend} disabled={loading}>{loading ? "Testing..." : "Gönder"}</button>
      </div>
      {provider && <p className="hint">Provider: {provider} · fallback: {String(Boolean(fallback))}</p>}
    </section>
  );
}
''',

    "frontend/admin/components/ProviderTest.jsx": '''export default function ProviderTest({ providers = {}, onTest, loading }) {
  return (
    <section className="card accent-yellow">
      <div className="card-header">
        <div>
          <p className="eyebrow">Diagnostics</p>
          <h2>Provider Test</h2>
          <p className="muted">Check configured provider status.</p>
        </div>
        <button className="btn ghost" onClick={onTest} disabled={loading}>{loading ? "Testing..." : "Test All"}</button>
      </div>
      <div className="provider-table">
        {Object.entries(providers).map(([name, info]) => (
          <div className="provider-row" key={name}>
            <strong>{name}</strong>
            <span className={info?.configured ? "status ok" : "status warn"}>{info?.configured ? "Configured" : "Missing"}</span>
            <small>{info?.masked || info?.env_key}</small>
          </div>
        ))}
      </div>
    </section>
  );
}
''',

    "frontend/admin/pages/ForgeAdmin.jsx": '''import { useEffect, useMemo, useState } from "react";
import AgentManager from "../components/AgentManager.jsx";
import LiveChatTest from "../components/LiveChatTest.jsx";
import MemoryManager from "../components/MemoryManager.jsx";
import PluginManager from "../components/PluginManager.jsx";
import ProjectManager from "../components/ProjectManager.jsx";
import ProviderManager from "../components/ProviderManager.jsx";
import ProviderTest from "../components/ProviderTest.jsx";
import SystemStatus from "../components/SystemStatus.jsx";
import TwitterDraftManager from "../components/TwitterDraftManager.jsx";

const API_BASE = "https://api.q-verse.io";

const sections = [
  { id: "dashboard", label: "Dashboard", subtitle: "Genel sistem özeti" },
  { id: "providers", label: "Providers", subtitle: "API key ve provider yönetimi" },
  { id: "projects", label: "Projects", subtitle: "Proje kayıt ve izleme" },
  { id: "agents", label: "Agents", subtitle: "Agent kayıt ve çalışma durumu" },
  { id: "plugins", label: "Plugins", subtitle: "Plugin ve entegrasyon kayıtları" },
  { id: "live-chat", label: "Live Chat", subtitle: "Canlı AI cevap testi" },
  { id: "memory", label: "Memory", subtitle: "Kalıcı hafıza kayıtları" },
  { id: "twitter", label: "Twitter/X", subtitle: "Güvenli sosyal medya taslakları" },
  { id: "system", label: "System Status", subtitle: "Ham sistem durumu ve JSON" },
];

export default function ForgeAdmin() {
  const [status, setStatus] = useState(null);
  const [activeSection, setActiveSection] = useState("dashboard");
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [projectName, setProjectName] = useState("");
  const [agentName, setAgentName] = useState("");
  const [pluginName, setPluginName] = useState("");
  const [memoryKey, setMemoryKey] = useState("");
  const [memoryValue, setMemoryValue] = useState("");
  const [draftText, setDraftText] = useState("");
  const [message, setMessage] = useState("");
  const [chatMessage, setChatMessage] = useState("Bu cevabı hangi provider üretiyor?");
  const [chatResult, setChatResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const providers = status?.provider_admin || {};
  const projects = status?.projects || {};
  const agents = status?.agents || {};
  const plugins = status?.plugins || {};

  const activeMeta = useMemo(() => sections.find((item) => item.id === activeSection) || sections[0], [activeSection]);

  async function refresh() {
    const res = await fetch(`${API_BASE}/forge/status`);
    setStatus(await res.json());
  }

  async function postJson(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();
    setMessage(JSON.stringify(data, null, 2));
    await refresh();
    return data;
  }

  async function saveProviderKey() {
    await postJson("/forge/providers/key", { provider, api_key: apiKey });
    setApiKey("");
  }

  async function addProject() {
    if (!projectName.trim()) return;
    await postJson("/forge/projects", { name: projectName, config: { source: "admin", status: "active" } });
    setProjectName("");
  }

  async function addAgent() {
    if (!agentName.trim()) return;
    await postJson("/forge/agents", { name: agentName, config: { source: "admin", status: "running" } });
    setAgentName("");
  }

  async function addPlugin() {
    if (!pluginName.trim()) return;
    await postJson("/forge/plugins", { name: pluginName, config: { source: "admin", enabled: true } });
    setPluginName("");
  }

  async function saveMemory() {
    if (!memoryKey.trim()) return;
    await postJson("/forge/memory/save", { namespace: "admin", key: memoryKey, value: memoryValue });
    setMemoryKey("");
    setMemoryValue("");
  }

  async function createTwitterDraft() {
    if (!draftText.trim()) return;
    await postJson("/forge/twitter/draft", { text: draftText });
    setDraftText("");
  }

  async function sendChatTest() {
    setLoading(true);
    try {
      const data = await postJson("/agents/chat", { message: chatMessage, source: "forge-admin", user_id: "admin" });
      setChatResult(data);
    } finally {
      setLoading(false);
    }
  }

  async function testProviders() {
    setLoading(true);
    try {
      await sendChatTest();
    } finally {
      setLoading(false);
    }
  }

  function showSection(id) {
    setActiveSection(id);
    window.history.replaceState(null, "", `#${id}`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  useEffect(() => {
    refresh();
    const initial = window.location.hash.replace("#", "");
    if (sections.some((item) => item.id === initial)) {
      setActiveSection(initial);
    }
    const onHashChange = () => {
      const next = window.location.hash.replace("#", "");
      if (sections.some((item) => item.id === next)) {
        setActiveSection(next);
      }
    };
    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="logo">Q</div><strong>Q-Verse Forge</strong></div>
        <nav>
          {sections.map((item) => (
            <button
              key={item.id}
              type="button"
              className={activeSection === item.id ? "active" : ""}
              onClick={() => showSection(item.id)}
              aria-current={activeSection === item.id ? "page" : undefined}
            >
              <span>{item.label}</span>
              <small>{item.subtitle}</small>
            </button>
          ))}
        </nav>
        <div className="sidebar-foot"><span className="dot ok"></span> Ultimate V12.2</div>
      </aside>

      <main className="dashboard">
        <header className="topbar" id="dashboard">
          <div>
            <p className="eyebrow">Q-Verse Platform</p>
            <h1>Q-Verse Forge Admin <span>V12.2</span></h1>
            <p className="muted"><strong>{activeMeta.label}</strong> — {activeMeta.subtitle}</p>
          </div>
          <div className="user-card"><span className="dot ok"></span> System Online</div>
        </header>
        <section className="section-banner">
          <div>
            <p className="eyebrow">Active Section</p>
            <h2>{activeMeta.label}</h2>
            <p className="muted">{activeMeta.subtitle}</p>
          </div>
          <span className="pill purple">#{activeSection}</span>
        </section>

        {activeSection === "dashboard" && (
          <>
            <section className="stats-grid">
              <div className="stat"><span>Providers</span><strong>{Object.keys(providers).length}</strong><small>Available</small></div>
              <div className="stat"><span>Projects</span><strong>{Object.keys(projects).length}</strong><small>Active</small></div>
              <div className="stat"><span>Agents</span><strong>{Object.keys(agents).length}</strong><small>Running</small></div>
              <div className="stat"><span>Plugins</span><strong>{Object.keys(plugins).length}</strong><small>Installed</small></div>
            </section>
            <section className="grid two">
              <ProviderManager provider={provider} setProvider={setProvider} apiKey={apiKey} setApiKey={setApiKey} onSave={saveProviderKey} providers={providers} />
              <LiveChatTest chatMessage={chatMessage} setChatMessage={setChatMessage} chatResult={chatResult} onSend={sendChatTest} loading={loading} />
            </section>
            <section className="grid two">
              <ProjectManager projectName={projectName} setProjectName={setProjectName} onAdd={addProject} projects={projects} />
              <ProviderTest providers={providers} onTest={testProviders} loading={loading} />
            </section>
          </>
        )}

        {activeSection === "providers" && <ProviderManager provider={provider} setProvider={setProvider} apiKey={apiKey} setApiKey={setApiKey} onSave={saveProviderKey} providers={providers} />}
        {activeSection === "projects" && <ProjectManager projectName={projectName} setProjectName={setProjectName} onAdd={addProject} projects={projects} />}
        {activeSection === "agents" && <AgentManager agentName={agentName} setAgentName={setAgentName} onAdd={addAgent} agents={agents} />}
        {activeSection === "plugins" && <PluginManager pluginName={pluginName} setPluginName={setPluginName} onAdd={addPlugin} plugins={plugins} />}
        {activeSection === "live-chat" && <LiveChatTest chatMessage={chatMessage} setChatMessage={setChatMessage} chatResult={chatResult} onSend={sendChatTest} loading={loading} />}
        {activeSection === "memory" && <MemoryManager memoryKey={memoryKey} setMemoryKey={setMemoryKey} memoryValue={memoryValue} setMemoryValue={setMemoryValue} onSave={saveMemory} />}
        {activeSection === "twitter" && <TwitterDraftManager draftText={draftText} setDraftText={setDraftText} onDraft={createTwitterDraft} />}
        {activeSection === "system" && <SystemStatus status={status} onRefresh={refresh} />}

        {message && <pre className="last-action">{message}</pre>}
      </main>
    </div>
  );
}
''',

    "frontend/admin/main.jsx": '''import React from "react";
import { createRoot } from "react-dom/client";
import ForgeAdmin from "./pages/ForgeAdmin.jsx";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ForgeAdmin />
  </React.StrictMode>
);
''',
    "frontend/admin/styles.css": ''':root {
  color-scheme: dark;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #07111f;
  color: #eef6ff;
}
* { box-sizing: border-box; }
html, body, #root { min-height: 100%; width: 100%; overflow-x: hidden; }
body { margin: 0; min-height: 100vh; background: radial-gradient(circle at top left, #123a68 0, transparent 34%), #07111f; }
button, input, select, textarea { font: inherit; }
button { cursor: pointer; }
.app-shell { display: grid; grid-template-columns: 280px minmax(0, 1fr); min-height: 100vh; width: 100%; max-width: 100vw; overflow-x: hidden; }
.sidebar { border-right: 1px solid rgba(148, 163, 184, 0.16); background: rgba(2, 8, 23, 0.72); backdrop-filter: blur(18px); padding: 24px; position: sticky; top: 0; height: 100vh; overflow: hidden; }
.brand { display: flex; align-items: center; gap: 12px; margin-bottom: 32px; }
.logo { width: 38px; height: 38px; border-radius: 12px; display: grid; place-items: center; background: linear-gradient(135deg, #2563eb, #7c3aed); font-weight: 900; flex: 0 0 auto; }
nav { display: grid; gap: 8px; }
nav button { width: 100%; text-align: left; padding: 12px 14px; border-radius: 12px; color: #aebbd0; text-decoration: none; background: transparent; border: 1px solid transparent; display: grid; gap: 3px; }
nav button.active, nav button:hover { background: rgba(37, 99, 235, 0.18); color: #60a5fa; }
nav button small { color: #64748b; font-size: 11px; line-height: 1.25; }
nav button.active { border-color: rgba(96, 165, 250, 0.35); box-shadow: inset 3px 0 0 #60a5fa; }
nav button.active small, nav button:hover small { color: #93c5fd; }
.sidebar-foot { position: absolute; bottom: 24px; left: 24px; right: 24px; padding: 16px; border-top: 1px solid rgba(148, 163, 184, 0.16); color: #aebbd0; }
.dashboard { min-width: 0; width: 100%; max-width: calc(100vw - 280px); padding: 34px; overflow-x: hidden; }
h1 { margin: 0; font-size: clamp(28px, 4vw, 34px); letter-spacing: -0.04em; }
h1 span { color: #93c5fd; font-size: 22px; }
h2 { margin: 0; font-size: 18px; }
.eyebrow { margin: 0 0 6px; text-transform: uppercase; letter-spacing: 0.12em; color: #60a5fa; font-size: 12px; font-weight: 800; }
.muted, .hint { color: #aebbd0; margin: 6px 0 0; }
.user-card, .pill { display: inline-flex; align-items: center; gap: 8px; border: 1px solid rgba(148, 163, 184, 0.18); background: rgba(15, 23, 42, 0.7); padding: 10px 14px; border-radius: 999px; color: #dbeafe; white-space: nowrap; }
.pill { font-size: 12px; padding: 7px 10px; }
.pill.ok, .status.ok { color: #34d399; }
.pill.warn, .status.warn { color: #fbbf24; }
.pill.purple { color: #c4b5fd; }
.dot { width: 10px; height: 10px; border-radius: 999px; display: inline-block; background: #64748b; flex: 0 0 auto; }
.dot.ok { background: #34d399; box-shadow: 0 0 18px #34d399; }
.stats-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-bottom: 18px; }
.stats-grid.compact { margin: 16px 0; }
.stat { min-width: 0; border: 1px solid rgba(148, 163, 184, 0.16); background: linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(15, 23, 42, 0.62)); border-radius: 16px; padding: 18px; }
.stat span, .stat small { color: #aebbd0; display: block; }
.stat strong { display: block; font-size: 30px; margin: 6px 0; }
.grid { display: grid; gap: 18px; margin-bottom: 18px; width: 100%; min-width: 0; }
.grid.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.card { min-width: 0; border: 1px solid rgba(148, 163, 184, 0.16); background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.55)); border-radius: 18px; padding: 20px; box-shadow: 0 18px 60px rgba(0, 0, 0, 0.22); overflow: hidden; }
.accent-blue { border-color: rgba(59, 130, 246, 0.32); }
.accent-green { border-color: rgba(52, 211, 153, 0.28); }
.accent-purple { border-color: rgba(139, 92, 246, 0.38); }
.accent-teal { border-color: rgba(45, 212, 191, 0.28); }
.accent-yellow { border-color: rgba(245, 158, 11, 0.30); }
.card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 18px; }
.form-row { display: flex; gap: 10px; align-items: center; min-width: 0; }
.form-row > input, .form-row > select { min-width: 0; }
input, select, textarea { width: 100%; border: 1px solid rgba(148, 163, 184, 0.18); background: rgba(2, 8, 23, 0.55); color: #eef6ff; border-radius: 12px; padding: 12px 13px; outline: none; }
input:focus, select:focus, textarea:focus { border-color: #60a5fa; box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.12); }
.btn { border: 1px solid rgba(148, 163, 184, 0.18); color: white; background: rgba(15, 23, 42, 0.78); border-radius: 12px; padding: 12px 15px; white-space: nowrap; flex: 0 0 auto; }
.btn.primary { background: linear-gradient(135deg, #2563eb, #7c3aed); border: 0; }
.btn.success { background: rgba(16, 185, 129, 0.18); border-color: rgba(16, 185, 129, 0.55); color: #34d399; }
.btn.purple { background: rgba(124, 58, 237, 0.32); border-color: rgba(167, 139, 250, 0.55); color: #ddd6fe; }
.btn.ghost { color: #bfdbfe; }
.btn.full { margin-top: 12px; width: 100%; }
.mini-list { list-style: none; padding: 0; margin: 16px 0 0; display: grid; gap: 10px; }
.mini-list li, .provider-row { display: flex; justify-content: space-between; gap: 12px; align-items: center; color: #eef6ff; min-width: 0; }
.mini-list b { color: #34d399; font-size: 12px; }
.chat-card { min-height: 420px; }
.chat-window { display: grid; gap: 12px; min-height: 220px; max-height: 360px; overflow-y: auto; border: 1px solid rgba(148, 163, 184, 0.12); background: rgba(2, 8, 23, 0.36); border-radius: 16px; padding: 16px; margin-bottom: 14px; }
.bubble { max-width: min(82%, 760px); padding: 14px 16px; border-radius: 16px; line-height: 1.5; overflow-wrap: anywhere; }
.bubble.user { justify-self: end; background: linear-gradient(135deg, #6d28d9, #2563eb); }
.bubble.bot { justify-self: start; background: rgba(30, 41, 59, 0.9); }
.provider-table { display: grid; border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 16px; overflow: hidden; }
.provider-row { padding: 14px; border-bottom: 1px solid rgba(148, 163, 184, 0.10); }
.provider-row small { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 45%; color: #cbd5e1; }
.provider-row:last-child { border-bottom: 0; }
.status-json, .last-action { background: #020617; color: #d1fae5; border-radius: 14px; padding: 16px; overflow: auto; max-height: 360px; max-width: 100%; border: 1px solid rgba(148, 163, 184, 0.14); }
.last-action { margin-top: 18px; }
.topbar { display: flex; justify-content: space-between; gap: 24px; align-items: flex-start; margin-bottom: 26px; }
.section-banner { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 18px; padding: 18px 20px; border-radius: 18px; border: 1px solid rgba(96, 165, 250, 0.24); background: linear-gradient(135deg, rgba(37, 99, 235, 0.16), rgba(124, 58, 237, 0.12)); }
h1 { margin: 0; font-size: clamp(28px, 4vw, 34px); letter-spacing: -0.04em; }
h1 span { color: #93c5fd; font-size: 22px; }
h2 { margin: 0; font-size: 18px; }
.eyebrow { margin: 0 0 6px; text-transform: uppercase; letter-spacing: 0.12em; color: #60a5fa; font-size: 12px; font-weight: 800; }
.muted, .hint { color: #aebbd0; margin: 6px 0 0; }
.user-card, .pill { display: inline-flex; align-items: center; gap: 8px; border: 1px solid rgba(148, 163, 184, 0.18); background: rgba(15, 23, 42, 0.7); padding: 10px 14px; border-radius: 999px; color: #dbeafe; white-space: nowrap; }
.pill { font-size: 12px; padding: 7px 10px; }
.pill.ok, .status.ok { color: #34d399; }
.pill.warn, .status.warn { color: #fbbf24; }
.pill.purple { color: #c4b5fd; }
.dot { width: 10px; height: 10px; border-radius: 999px; display: inline-block; background: #64748b; flex: 0 0 auto; }
.dot.ok { background: #34d399; box-shadow: 0 0 18px #34d399; }
.stats-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-bottom: 18px; }
.stats-grid.compact { margin: 16px 0; }
.stat { min-width: 0; border: 1px solid rgba(148, 163, 184, 0.16); background: linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(15, 23, 42, 0.62)); border-radius: 16px; padding: 18px; }
.stat span, .stat small { color: #aebbd0; display: block; }
.stat strong { display: block; font-size: 30px; margin: 6px 0; }
.grid { display: grid; gap: 18px; margin-bottom: 18px; width: 100%; min-width: 0; }
.grid.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.grid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.card { min-width: 0; border: 1px solid rgba(148, 163, 184, 0.16); background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.55)); border-radius: 18px; padding: 20px; box-shadow: 0 18px 60px rgba(0, 0, 0, 0.22); overflow: hidden; }
.accent-blue { border-color: rgba(59, 130, 246, 0.32); }
.accent-green { border-color: rgba(52, 211, 153, 0.28); }
.accent-purple { border-color: rgba(139, 92, 246, 0.38); }
.accent-teal { border-color: rgba(45, 212, 191, 0.28); }
.accent-yellow { border-color: rgba(245, 158, 11, 0.30); }
.card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 18px; }
.form-row { display: flex; gap: 10px; align-items: center; min-width: 0; }
.form-row > input, .form-row > select { min-width: 0; }
input, select, textarea { width: 100%; border: 1px solid rgba(148, 163, 184, 0.18); background: rgba(2, 8, 23, 0.55); color: #eef6ff; border-radius: 12px; padding: 12px 13px; outline: none; }
input:focus, select:focus, textarea:focus { border-color: #60a5fa; box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.12); }
.btn { border: 1px solid rgba(148, 163, 184, 0.18); color: white; background: rgba(15, 23, 42, 0.78); border-radius: 12px; padding: 12px 15px; white-space: nowrap; flex: 0 0 auto; }
.btn.primary { background: linear-gradient(135deg, #2563eb, #7c3aed); border: 0; }
.btn.success { background: rgba(16, 185, 129, 0.18); border-color: rgba(16, 185, 129, 0.55); color: #34d399; }
.btn.purple { background: rgba(124, 58, 237, 0.32); border-color: rgba(167, 139, 250, 0.55); color: #ddd6fe; }
.btn.ghost { color: #bfdbfe; }
.btn.full { margin-top: 12px; width: 100%; }
.mini-list { list-style: none; padding: 0; margin: 16px 0 0; display: grid; gap: 10px; }
.mini-list li, .provider-row { display: flex; justify-content: space-between; gap: 12px; align-items: center; color: #eef6ff; min-width: 0; }
.mini-list b { color: #34d399; font-size: 12px; }
.chat-card { min-height: 420px; }
.chat-window { display: grid; gap: 12px; min-height: 220px; max-height: 360px; overflow-y: auto; border: 1px solid rgba(148, 163, 184, 0.12); background: rgba(2, 8, 23, 0.36); border-radius: 16px; padding: 16px; margin-bottom: 14px; }
.bubble { max-width: min(82%, 760px); padding: 14px 16px; border-radius: 16px; line-height: 1.5; overflow-wrap: anywhere; }
.bubble.user { justify-self: end; background: linear-gradient(135deg, #6d28d9, #2563eb); }
.bubble.bot { justify-self: start; background: rgba(30, 41, 59, 0.9); }
.provider-table { display: grid; border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 16px; overflow: hidden; }
.provider-row { padding: 14px; border-bottom: 1px solid rgba(148, 163, 184, 0.10); }
.provider-row small { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 45%; color: #cbd5e1; }
.provider-row:last-child { border-bottom: 0; }
.status-json, .last-action { background: #020617; color: #d1fae5; border-radius: 14px; padding: 16px; overflow: auto; max-height: 360px; max-width: 100%; border: 1px solid rgba(148, 163, 184, 0.14); }
.last-action { margin-top: 18px; }
@media (max-width: 1400px) { .grid.four { grid-template-columns: repeat(2, minmax(0, 1fr)); } .stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 900px) { .app-shell { grid-template-columns: 1fr; } .sidebar { position: relative; height: auto; } .sidebar-foot { position: static; margin-top: 24px; } .dashboard { max-width: 100vw; padding: 22px; } .grid.four, .grid.two, .stats-grid { grid-template-columns: 1fr; } .topbar, .section-banner { flex-direction: column; align-items: stretch; } .form-row { flex-direction: column; align-items: stretch; } }
''',

    "frontend/admin/index.html": '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Q-Verse Forge Admin</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="./main.jsx"></script>
  </body>
</html>
''',

    "frontend/admin/vite.config.js": '''import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  root: ".",
  base: "/admin/forge/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
''',

    "frontend/admin/package.json": json.dumps({
        "name": "qverse-forge-admin",
        "version": "12.1.0",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "vite --host 0.0.0.0 --port 5174",
            "build": "vite build",
            "preview": "vite preview --host 0.0.0.0 --port 4174"
        },
        "dependencies": {
            "@vitejs/plugin-react": "^4.3.4",
            "vite": "^5.4.11",
            "react": "latest",
            "react-dom": "latest"
        },
        "devDependencies": {}
    }, indent=2) + "\n",

    "frontend/admin/.env.example": '''VITE_QVERSE_API_BASE=https://api.q-verse.io
''',

    "frontend/admin/README.md": '''# Q-Verse Forge Admin UI

This is the web admin interface for Q-Verse Forge.

## Local development

```bash
cd frontend/admin
npm install
npm run dev
```

## Production build

```bash
cd frontend/admin
npm install
npm run build
```

Deploy the generated `dist` directory behind Nginx, for example under:

```text
https://api.q-verse.io/admin/forge/
```

The frontend talks to:

```text
https://api.q-verse.io/forge
```
''',

    "deploy/nginx/forge-admin.conf": '''# Optional Nginx location for Q-Verse Forge Admin UI
# Add this inside the api.q-verse.io server block after building frontend/admin/dist.

location /admin/forge/ {
    alias /opt/qverse-platform/frontend/admin/dist/;
    index index.html;
    try_files $uri $uri/ /admin/forge/index.html;
}
''',

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
- Provider Manager UI
- Project Manager UI
- Agent Manager UI
- Plugin Manager UI
- Memory Manager UI
- Twitter Draft Manager UI
- Forge Admin Vite App
- Forge Admin Nginx Deploy Snippet
- Live Chat Test UI
- Provider Test UI
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
        "ai/response/AIResponseEngine.py",
        "frontend/admin/components/LiveChatTest.jsx",
        "frontend/admin/components/ProviderTest.jsx",
        "frontend/admin/styles.css",
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
            "/admin/forge/",
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