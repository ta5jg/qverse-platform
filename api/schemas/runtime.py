from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class RuntimeEnvironment(VersionMixin, BaseModel):
    environment: str = "development"
    platform: str
    python_version: str
    hostname: Optional[str] = None


class RuntimeProcess(BaseModel):
    pid: int
    name: str
    status: str = "running"
    memory_mb: float = 0.0
    cpu_percent: float = 0.0


class RuntimeResponse(VersionMixin, BaseModel):
    runtime_id: str
    status: str = "running"
    environment: RuntimeEnvironment


class RuntimeRegistryResponse(VersionMixin, BaseModel):
    runtimes: List[RuntimeResponse] = Field(default_factory=list)
    total: int = 0


class RuntimeSnapshotResponse(TimestampMixin, BaseModel):
    snapshot_id: str
    processes: List[RuntimeProcess] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class RuntimeMetricsResponse(BaseModel):
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_percent: float = 0.0
    active_processes: int = 0
    threads: int = 0
    extra: Dict[str, float] = Field(default_factory=dict)


class RuntimeExecutionResponse(TimestampMixin, BaseModel):
    execution_id: str
    action: str
    success: bool = True
    execution_time_ms: float = 0.0


class RuntimeAuditResponse(BaseModel):
    runtime_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RuntimeHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    runtime_available: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)
