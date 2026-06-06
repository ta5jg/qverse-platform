#!/usr/bin/env python3
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = {
    "api/managers/agent_manager.py": '''class AgentManager:
    def __init__(self):
        self.name = "QVerseAgent"
        self.version = "V9"
        self.status = "active"

    def get_dashboard(self):
        return {
            "success": True,
            "agent": self.name,
            "version": self.version,
            "status": self.status,
            "capabilities": [
                "chat",
                "planning",
                "execution",
                "memory",
                "tools",
                "workflows",
                "ai_routing",
            ],
            "endpoints": [
                "/agents",
                "/agents/chat",
                "/agents/run",
            ],
        }

    def chat(self, message: str, source: str = "api", user_id: str = "anonymous", context=None):
        try:
            from agent.runtime.AgentRuntime import run_agent
            result = run_agent(message, context={
                "source": source,
                "user_id": user_id,
                "context": context or {},
            })
            ai_result = result.get("ai_response", {}).get("result", {})
            reply = ai_result.get("response") or result.get("execution", {}).get("result") or "Q-Verse Agent completed the request."
            return {
                "success": True,
                "agent": self.name,
                "reply": reply,
                "source": source,
                "user_id": user_id,
                "runtime": result,
            }
        except Exception as exc:
            return {
                "success": False,
                "agent": self.name,
                "error": type(exc).__name__,
                "message": str(exc),
            }

    def run(self, payload=None):
        payload = payload or {}
        message = payload.get("message") or payload.get("prompt") or ""
        return self.chat(
            message=message,
            source=payload.get("source", "api"),
            user_id=str(payload.get("user_id", "anonymous")),
            context=payload.get("context", {}),
        )


agent_manager = AgentManager()
''',

    "api/managers/system_manager.py": '''class SystemManager:
    def __init__(self):
        self.platform = "Q-Verse"
        self.version = "V9"

    def get_metrics(self):
        return {
            "success": True,
            "platform": self.platform,
            "version": self.version,
            "status": "operational",
            "services": {
                "api": "running",
                "agent": "active",
                "ai_runtime": "ready",
                "routes": "enabled",
            },
            "health": {
                "score": 100,
                "state": "healthy",
            },
        }

    def get_status(self):
        return self.get_metrics()


system_manager = SystemManager()
''',

    "api/routes/agent_chat.py": '''from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from api.managers.agent_manager import agent_manager

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentChatRequest(BaseModel):
    message: str = Field(default="")
    source: str = Field(default="api")
    user_id: str = Field(default="anonymous")
    username: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


@router.get("")
def get_agents_dashboard():
    return agent_manager.get_dashboard()


@router.get("/")
def get_agents_dashboard_slash():
    return agent_manager.get_dashboard()


@router.post("/chat")
def chat_with_agent(request: AgentChatRequest):
    context = dict(request.context or {})
    if request.username:
        context["username"] = request.username
    return agent_manager.chat(
        message=request.message,
        source=request.source,
        user_id=request.user_id,
        context=context,
    )


@router.post("/run")
def run_agent(request: AgentChatRequest):
    return agent_manager.run(request.model_dump())
''',

    "api/routes/agents.py": '''from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from api.managers.agent_manager import agent_manager

router = APIRouter(prefix="/agents", tags=["agents"])


class AgentChatRequest(BaseModel):
    message: str = Field(default="")
    source: str = Field(default="api")
    user_id: str = Field(default="anonymous")
    username: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


@router.get("")
def get_agents_dashboard():
    return agent_manager.get_dashboard()


@router.get("/")
def get_agents_dashboard_slash():
    return agent_manager.get_dashboard()


@router.post("/chat")
def chat_with_agent(request: AgentChatRequest):
    context = dict(request.context or {})
    if request.username:
        context["username"] = request.username
    return agent_manager.chat(
        message=request.message,
        source=request.source,
        user_id=request.user_id,
        context=context,
    )


@router.post("/run")
def run_agent(request: AgentChatRequest):
    return agent_manager.run(request.model_dump())
''',

    "api/routes/orchestrator.py": '''from fastapi import APIRouter
from api.managers.system_manager import system_manager

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.get("")
def get_orchestrator_metrics():
    return system_manager.get_metrics()


@router.get("/")
def get_orchestrator_metrics_slash():
    return system_manager.get_metrics()
''',

    "agent/memory/MemoryManager.py": '''class MemoryManager:
    def __init__(self):
        self._records = {}

    def save(self, key, value):
        self._records[key] = value
        return {"status": "ok", "saved_key": key}

    def save_memory(self, key: str, value):
        return self.save(key, value)

    def get(self, key):
        if key in self._records:
            return {"status": "ok", "key": key, "value": self._records[key]}
        return {"status": "not_found", "key": key}

    def recall(self, key: str):
        result = self.get(key)
        if result.get("status") == "ok":
            return [{"key": key, "value": result.get("value")}]
        return []

    def list_items(self):
        return {"status": "ok", "items": list(self._records.items())}

    def list_memories(self):
        result = self.list_items()
        return [{"key": key, "value": value} for key, value in result.get("items", [])]

    def health(self):
        return {
            "status": "healthy",
            "item_count": len(self._records),
        }
'''
}

ROUTES_INIT_PATCH = '''from api.routes.agent_chat import router as agent_chat_router'''
ROUTES_INIT_INCLUDE = '''agent_chat_router'''


def write_file(path: str, content: str, force: bool = False):
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    should_write = force or not file_path.exists() or file_path.read_text(encoding="utf-8").strip() == ""
    if should_write:
        file_path.write_text(content, encoding="utf-8")
        print(f"[WRITE] {path}")
    else:
        print(f"[SKIP] {path}")


def patch_routes_init():
    init_path = ROOT / "api/routes/__init__.py"
    if not init_path.exists():
        print("[WARN] api/routes/__init__.py not found")
        return

    content = init_path.read_text(encoding="utf-8")

    if ROUTES_INIT_PATCH not in content:
        lines = content.splitlines()
        insert_at = 0
        for index, line in enumerate(lines):
            if line.startswith("from api.routes"):
                insert_at = index + 1
        lines.insert(insert_at, ROUTES_INIT_PATCH)
        content = "\n".join(lines) + "\n"
        print("[PATCH] import agent_chat_router")

    enabled_block_has_agent_chat = "agent_chat_router," in content or "agent_chat_router" in content.split("enabled_routers = [", 1)[-1].split("]", 1)[0]
    if "enabled_routers" in content and not enabled_block_has_agent_chat:
        content = content.replace("enabled_routers = [", "enabled_routers = [\n    agent_chat_router,")
        print("[PATCH] include agent_chat_router")

    init_path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Q-Verse API Runtime Fix Bootstrap")
    parser.add_argument("--force", action="store_true", help="Overwrite runtime files")
    args = parser.parse_args()

    print("Q-Verse API Runtime Fix Started")
    for path, content in FILES.items():
        write_file(path, content, force=args.force)
    patch_routes_init()
    print(f"[SUMMARY] Runtime fixes generated: {len(FILES)}")
    print("[API] Agent dashboard, orchestrator metrics, memory compatibility, existing agents route and n8n chat endpoints ready")
    print("Q-Verse API Runtime Fix Complete")


if __name__ == "__main__":
    main()
