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
    return audit_logger.log(event, payload)\n