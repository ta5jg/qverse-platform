

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class ServiceEndpoint(BaseModel):
    path: str
    method: str
    authenticated: bool = False


class ServiceResponse(VersionMixin, BaseModel):
    service_id: str
    name: str
    status: str = "running"
    version: str = "V9"
    endpoints: List[ServiceEndpoint] = Field(default_factory=list)


class ServiceCreateRequest(BaseModel):
    name: str
    status: str = "running"


class ServiceUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class ServiceRegistryResponse(VersionMixin, BaseModel):
    services: List[ServiceResponse] = Field(default_factory=list)
    total: int = 0


class ServiceExecutionResponse(TimestampMixin, BaseModel):
    execution_id: str
    service_id: str
    success: bool = True
    completed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0


class ServiceMetricsResponse(BaseModel):
    total_services: int = 0
    active_services: int = 0
    failed_services: int = 0
    requests_processed: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class ServiceAuditResponse(BaseModel):
    service_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ServiceHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    service_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)