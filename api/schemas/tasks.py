

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.enums import TaskStatus
from api.schemas.mixins import TimestampMixin, VersionMixin


class TaskPayload(BaseModel):
    command: Optional[str] = None
    parameters: Dict[str, str] = Field(default_factory=dict)


class TaskResponse(VersionMixin, BaseModel):
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 5
    payload: TaskPayload = Field(default_factory=TaskPayload)


class TaskCreateRequest(BaseModel):
    name: str
    priority: int = 5
    payload: TaskPayload = Field(default_factory=TaskPayload)


class TaskUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    payload: Optional[TaskPayload] = None


class TaskQueueResponse(VersionMixin, BaseModel):
    pending_tasks: int = 0
    running_tasks: int = 0
    failed_tasks: int = 0
    queue_available: bool = True


class TaskRegistryResponse(VersionMixin, BaseModel):
    tasks: List[TaskResponse] = Field(default_factory=list)
    total: int = 0


class TaskExecutionResponse(TimestampMixin, BaseModel):
    execution_id: str
    task_id: str
    success: bool = True
    status: TaskStatus = TaskStatus.COMPLETED
    completed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0


class TaskMetricsResponse(BaseModel):
    total_tasks: int = 0
    pending_tasks: int = 0
    running_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class TaskAuditResponse(BaseModel):
    task_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TaskHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    task_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)