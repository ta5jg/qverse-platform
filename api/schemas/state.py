

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class StateEntry(VersionMixin, BaseModel):
    key: str
    value: str
    namespace: str = "default"
    description: Optional[str] = None


class StateSnapshotResponse(TimestampMixin, BaseModel):
    snapshot_id: str
    entries: List[StateEntry] = Field(default_factory=list)
    total: int = 0


class StateCreateRequest(BaseModel):
    key: str
    value: str
    namespace: str = "default"


class StateUpdateRequest(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None


class StateRegistryResponse(VersionMixin, BaseModel):
    states: List[StateEntry] = Field(default_factory=list)
    total: int = 0


class StateMetricsResponse(BaseModel):
    total_entries: int = 0
    namespaces: int = 0
    snapshots: int = 0
    updates: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class StateAuditResponse(BaseModel):
    key: str
    action: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StateHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    state_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)