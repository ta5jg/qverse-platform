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
  return (
    <section style={{ marginTop: 24 }}>
      <h2>System Status</h2>
      <button onClick={onRefresh}>Refresh</button>
      <pre style={{ background: "#111", color: "#0f0", padding: 16, overflow: "auto" }}>
        {JSON.stringify(status, null, 2)}
      </pre>
    </section>
  );
}
''',

    "frontend/admin/components/ProviderManager.jsx": '''export default function ProviderManager({ provider, setProvider, apiKey, setApiKey, onSave }) {
  return (
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
      <button onClick={onSave} style={{ marginLeft: 8 }}>Save Key</button>
    </section>
  );
}
''',

    "frontend/admin/components/ProjectManager.jsx": '''export default function ProjectManager({ projectName, setProjectName, onAdd }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Projects</h2>
      <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project name" />
      <button onClick={onAdd} style={{ marginLeft: 8 }}>Add Project</button>
    </section>
  );
}
''',

    "frontend/admin/components/AgentManager.jsx": '''export default function AgentManager({ agentName, setAgentName, onAdd }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Agents</h2>
      <input value={agentName} onChange={(e) => setAgentName(e.target.value)} placeholder="Agent name" />
      <button onClick={onAdd} style={{ marginLeft: 8 }}>Add Agent</button>
    </section>
  );
}
''',

    "frontend/admin/components/PluginManager.jsx": '''export default function PluginManager({ pluginName, setPluginName, onAdd }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Plugins</h2>
      <input value={pluginName} onChange={(e) => setPluginName(e.target.value)} placeholder="Plugin name" />
      <button onClick={onAdd} style={{ marginLeft: 8 }}>Add Plugin</button>
    </section>
  );
}
''',

    "frontend/admin/components/MemoryManager.jsx": '''export default function MemoryManager({ memoryKey, setMemoryKey, memoryValue, setMemoryValue, onSave }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Memory</h2>
      <input value={memoryKey} onChange={(e) => setMemoryKey(e.target.value)} placeholder="Memory key" />
      <input
        value={memoryValue}
        onChange={(e) => setMemoryValue(e.target.value)}
        placeholder="Memory value"
        style={{ marginLeft: 8, width: 360 }}
      />
      <button onClick={onSave} style={{ marginLeft: 8 }}>Save Memory</button>
    </section>
  );
}
''',

    "frontend/admin/components/TwitterDraftManager.jsx": '''export default function TwitterDraftManager({ draftText, setDraftText, onDraft }) {
  return (
    <section style={{ marginTop: 24 }}>
      <h2>Twitter/X Draft Queue</h2>
      <textarea
        value={draftText}
        onChange={(e) => setDraftText(e.target.value)}
        placeholder="Draft safe-mode post"
        rows={4}
        style={{ width: "100%" }}
      />
      <button onClick={onDraft} style={{ marginTop: 8 }}>Create Draft</button>
    </section>
  );
}
''',

    "frontend/admin/pages/ForgeAdmin.jsx": '''import { useEffect, useState } from "react";
import AgentManager from "../components/AgentManager.jsx";
import MemoryManager from "../components/MemoryManager.jsx";
import PluginManager from "../components/PluginManager.jsx";
import ProjectManager from "../components/ProjectManager.jsx";
import ProviderManager from "../components/ProviderManager.jsx";
import SystemStatus from "../components/SystemStatus.jsx";
import TwitterDraftManager from "../components/TwitterDraftManager.jsx";

const API_BASE = "https://api.q-verse.io";

export default function ForgeAdmin() {
  const [status, setStatus] = useState(null);
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [projectName, setProjectName] = useState("");
  const [agentName, setAgentName] = useState("");
  const [pluginName, setPluginName] = useState("");
  const [memoryKey, setMemoryKey] = useState("");
  const [memoryValue, setMemoryValue] = useState("");
  const [draftText, setDraftText] = useState("");
  const [message, setMessage] = useState("");

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
    await postJson("/forge/projects", { name: projectName, config: { source: "admin" } });
    setProjectName("");
  }

  async function addAgent() {
    await postJson("/forge/agents", { name: agentName, config: { source: "admin" } });
    setAgentName("");
  }

  async function addPlugin() {
    await postJson("/forge/plugins", { name: pluginName, config: { source: "admin" } });
    setPluginName("");
  }

  async function saveMemory() {
    await postJson("/forge/memory/save", { namespace: "admin", key: memoryKey, value: memoryValue });
    setMemoryKey("");
    setMemoryValue("");
  }

  async function createTwitterDraft() {
    await postJson("/forge/twitter/draft", { text: draftText });
    setDraftText("");
  }

  useEffect(() => { refresh(); }, []);

  return (
    <main style={{ padding: 24, fontFamily: "system-ui", maxWidth: 1100 }}>
      <h1>Q-Verse Forge Admin V12.1</h1>
      <p>Manage providers, API keys, projects, agents, plugins, workflows, memory and integrations.</p>

      <ProviderManager provider={provider} setProvider={setProvider} apiKey={apiKey} setApiKey={setApiKey} onSave={saveProviderKey} />
      <ProjectManager projectName={projectName} setProjectName={setProjectName} onAdd={addProject} />
      <AgentManager agentName={agentName} setAgentName={setAgentName} onAdd={addAgent} />
      <PluginManager pluginName={pluginName} setPluginName={setPluginName} onAdd={addPlugin} />
      <MemoryManager memoryKey={memoryKey} setMemoryKey={setMemoryKey} memoryValue={memoryValue} setMemoryValue={setMemoryValue} onSave={saveMemory} />
      <TwitterDraftManager draftText={draftText} setDraftText={setDraftText} onDraft={createTwitterDraft} />
      <SystemStatus status={status} onRefresh={refresh} />

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

    "frontend/admin/main.jsx": '''import React from "react";
import { createRoot } from "react-dom/client";
import ForgeAdmin from "./pages/ForgeAdmin.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ForgeAdmin />
  </React.StrictMode>
);
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
    <script type="module" src="/main.jsx"></script>
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