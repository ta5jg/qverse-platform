from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class ProjectMetadata(TimestampMixin, BaseModel):
    tags: List[str] = Field(default_factory=list)
    owner: Optional[str] = None
    repository: Optional[str] = None


class ProjectResponse(VersionMixin, BaseModel):
    project_id: str
    name: str
    description: Optional[str] = None
    status: str = "active"
    metadata: ProjectMetadata = Field(default_factory=ProjectMetadata)


class ProjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None


class ProjectRegistryResponse(VersionMixin, BaseModel):
    projects: List[ProjectResponse] = Field(default_factory=list)
    total: int = 0


class ProjectStatusResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    project_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)


class ProjectMetricsResponse(BaseModel):
    total_projects: int = 0
    active_projects: int = 0
    archived_projects: int = 0
    failed_projects: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class ProjectHealthResponse(TimestampMixin, BaseModel):
    status: str = "ok"
    projects_available: bool = True


class ProjectAuditResponse(BaseModel):
    project_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
