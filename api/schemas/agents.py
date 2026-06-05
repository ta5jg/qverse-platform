from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.enums import AgentStatus
from api.schemas.mixins import TimestampMixin, VersionMixin


class AgentCapability(VersionMixin, BaseModel):
    name: str
    enabled: bool = True
    description: Optional[str] = None


class AgentResponse(VersionMixin, BaseModel):
    agent_id: str
    name: str
    status: AgentStatus = AgentStatus.IDLE
    capabilities: List[AgentCapability] = Field(default_factory=list)


class AgentCreateRequest(BaseModel):
    name: str
    capabilities: List[str] = Field(default_factory=list)


class AgentUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[AgentStatus] = None


class AgentRegistryResponse(VersionMixin, BaseModel):
    agents: List[AgentResponse] = Field(default_factory=list)
    total: int = 0


class AgentExecutionResponse(TimestampMixin, BaseModel):
    execution_id: str
    agent_id: str
    success: bool = True
    completed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0


class AgentHealthResponse(TimestampMixin, BaseModel):
    status: str = "ok"
    agent_available: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)


class AgentMetricsResponse(BaseModel):
    total_agents: int = 0
    active_agents: int = 0
    idle_agents: int = 0
    failed_agents: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class AgentAuditResponse(BaseModel):
    agent_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentStatusResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    agent_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)