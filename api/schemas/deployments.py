

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.enums import DeploymentStatus
from api.schemas.mixins import TimestampMixin, VersionMixin


class DeploymentTarget(BaseModel):
    environment: str
    region: Optional[str] = None
    cluster: Optional[str] = None


class DeploymentResponse(VersionMixin, BaseModel):
    deployment_id: str
    name: str
    version_tag: str
    status: DeploymentStatus = DeploymentStatus.PENDING
    target: DeploymentTarget


class DeploymentCreateRequest(BaseModel):
    name: str
    version_tag: str
    target: DeploymentTarget


class DeploymentUpdateRequest(BaseModel):
    status: Optional[DeploymentStatus] = None
    version_tag: Optional[str] = None


class DeploymentRegistryResponse(VersionMixin, BaseModel):
    deployments: List[DeploymentResponse] = Field(default_factory=list)
    total: int = 0


class DeploymentExecutionResponse(TimestampMixin, BaseModel):
    execution_id: str
    deployment_id: str
    success: bool = True
    status: DeploymentStatus = DeploymentStatus.DEPLOYED
    completed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0


class DeploymentMetricsResponse(BaseModel):
    total_deployments: int = 0
    successful_deployments: int = 0
    failed_deployments: int = 0
    rollbacks: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class DeploymentAuditResponse(BaseModel):
    deployment_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DeploymentHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    deployment_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)