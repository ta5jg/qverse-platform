from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.enums import WorkflowStatus
from api.schemas.mixins import TimestampMixin, VersionMixin


class WorkflowStep(VersionMixin, BaseModel):
    step_id: str
    name: str
    status: str = "pending"
    description: Optional[str] = None


class WorkflowResponse(VersionMixin, BaseModel):
    workflow_id: str
    name: str
    enabled: bool = True
    status: WorkflowStatus = WorkflowStatus.ACTIVE
    steps: List[WorkflowStep] = Field(default_factory=list)


class WorkflowCreateRequest(BaseModel):
    name: str
    enabled: bool = True


class WorkflowUpdateRequest(BaseModel):
    name: Optional[str] = None
    enabled: Optional[bool] = None
    status: Optional[WorkflowStatus] = None


class WorkflowRegistryResponse(VersionMixin, BaseModel):
    workflows: List[WorkflowResponse] = Field(default_factory=list)
    total: int = 0


class WorkflowExecutionResponse(TimestampMixin, BaseModel):
    execution_id: str
    workflow_id: str
    success: bool = True
    completed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0


class WorkflowHealthResponse(TimestampMixin, BaseModel):
    status: str = "ok"
    workflow_available: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)


class WorkflowMetricsResponse(BaseModel):
    total_workflows: int = 0
    active_workflows: int = 0
    executions: int = 0
    failed_executions: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class WorkflowAuditResponse(BaseModel):
    workflow_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WorkflowStatusResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    workflow_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)
