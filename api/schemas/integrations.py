

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class IntegrationProvider(VersionMixin, BaseModel):
    provider_id: str
    name: str
    enabled: bool = True
    description: Optional[str] = None


class IntegrationResponse(VersionMixin, BaseModel):
    integration_id: str
    provider: str
    status: str = "connected"
    metadata: Dict[str, str] = Field(default_factory=dict)


class IntegrationCreateRequest(BaseModel):
    provider: str
    metadata: Dict[str, str] = Field(default_factory=dict)


class IntegrationUpdateRequest(BaseModel):
    status: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class IntegrationRegistryResponse(VersionMixin, BaseModel):
    integrations: List[IntegrationResponse] = Field(default_factory=list)
    total: int = 0


class IntegrationHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    integration_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)


class IntegrationSyncResponse(TimestampMixin, BaseModel):
    sync_id: str
    integration_id: str
    success: bool = True
    completed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0


class IntegrationMetricsResponse(BaseModel):
    total_integrations: int = 0
    active_integrations: int = 0
    failed_integrations: int = 0
    sync_operations: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class IntegrationAuditResponse(BaseModel):
    integration_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)