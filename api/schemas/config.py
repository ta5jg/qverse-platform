

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class ConfigEntry(VersionMixin, BaseModel):
    key: str
    value: str
    category: str = "general"
    description: Optional[str] = None
    sensitive: bool = False


class ConfigCreateRequest(BaseModel):
    key: str
    value: str
    category: str = "general"
    description: Optional[str] = None


class ConfigUpdateRequest(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    sensitive: Optional[bool] = None


class ConfigRegistryResponse(VersionMixin, BaseModel):
    configs: List[ConfigEntry] = Field(default_factory=list)
    total: int = 0


class ConfigSnapshotResponse(TimestampMixin, BaseModel):
    snapshot_id: str
    entries: int = 0
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class ConfigMetricsResponse(BaseModel):
    total_configs: int = 0
    categories: int = 0
    sensitive_configs: int = 0
    updates: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class ConfigAuditResponse(BaseModel):
    key: str
    action: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConfigHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    config_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)