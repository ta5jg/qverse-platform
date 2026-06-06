from fastapi import APIRouter
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
