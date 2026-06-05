

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class AdminUser(VersionMixin, BaseModel):
    user_id: str
    username: str
    role: str = "admin"
    active: bool = True
    email: Optional[str] = None


class AdminCreateRequest(BaseModel):
    username: str
    role: str = "admin"
    email: Optional[str] = None


class AdminUpdateRequest(BaseModel):
    role: Optional[str] = None
    active: Optional[bool] = None
    email: Optional[str] = None


class AdminRegistryResponse(VersionMixin, BaseModel):
    admins: List[AdminUser] = Field(default_factory=list)
    total: int = 0


class AdminActionResponse(TimestampMixin, BaseModel):
    action_id: str
    action: str
    success: bool = True
    execution_time_ms: float = 0.0


class AdminPermissionResponse(BaseModel):
    user_id: str
    permissions: List[str] = Field(default_factory=list)


class AdminMetricsResponse(BaseModel):
    total_admins: int = 0
    active_admins: int = 0
    actions_executed: int = 0
    failed_actions: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class AdminAuditResponse(BaseModel):
    user_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AdminHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    admin_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)