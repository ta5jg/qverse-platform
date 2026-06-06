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

    "memory/vector/VectorMemory.py": '''
class VectorMemory:
    def __init__(self):
        self.items = []

    def add(self, text, metadata=None):
        item = {"id": len(self.items) + 1, "text": text, "metadata": metadata or {}}
        self.items.append(item)
        return item

    def search(self, query, limit=5):
        hits = [item for item in self.items if query.lower() in item["text"].lower()]
        return hits[:limit]

vector_memory = VectorMemory()
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

@router.get("/status")
def status():
    return {
        "status": "ready",
        "providers": provider_health_cache.status(),
        "tasks": task_queue.list(),
        "events": event_bus.list_events(),
        "agents": agent_registry.list_agents(),
        "projects": project_registry.list_projects(),
        "plugins": plugin_registry.list_plugins(),
    }

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

    "frontend/admin/pages/ForgeAdmin.jsx": '''
export default function ForgeAdmin() {
  return (
    <main style={{ padding: 24 }}>
      <h1>Q-Verse Forge Admin</h1>
      <p>Manage providers, API keys, projects, agents, plugins, workflows, memory and integrations.</p>
      <ul>
        <li>Provider Management</li>
        <li>API Key Management</li>
        <li>Project Registry</li>
        <li>Agent Registry</li>
        <li>Plugin System</li>
        <li>Memory Explorer</li>
        <li>Twitter Draft Queue</li>
        <li>GitHub Webhooks</li>
      </ul>
    </main>
  );
}
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
    target.write_text(content.strip() + "\\n", encoding="utf-8")
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
        text = text.replace("enabled_routers = [", "enabled_routers = [\\n    forge_router,")

    init_path.write_text(text, encoding="utf-8")
    return {"patched": True}


def scan_project():
    required = list(FILES.keys())
    missing = [p for p in required if not (ROOT / p).exists()]
    return {"required": len(required), "missing": missing, "missing_count": len(missing)}


def run_compile_checks():
    checks = [
        "api/routes/forge.py",
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


def write_report(written, skipped, scan, route_patch, compile_results):
    report = {
        "version": VERSION,
        "status": "forge_complete",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "written_count": len(written),
        "skipped_count": len(skipped),
        "written": written,
        "skipped": skipped,
        "scan": scan,
        "route_patch": route_patch,
        "compile": compile_results,
        "endpoints": [
            "/forge/status",
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

    route_patch = {"patched": False, "reason": "disabled"}
    if not args.no_patch_routes:
        route_patch = patch_routes_init()
        print(f"[ROUTES] {route_patch}")

    compile_results = run_compile_checks()
    report_path = write_report(written, skipped, scan_before, route_patch, compile_results)

    print(f"[SUMMARY] written={len(written)} skipped={len(skipped)}")
    print(f"[REPORT] {report_path.relative_to(ROOT)}")
    print("Q-Verse Forge Complete")


if __name__ == "__main__":
    main()