from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class SystemInfoResponse(VersionMixin, TimestampMixin):
    platform: str
    api: str
    environment: str = "development"


class RuntimeInfoResponse(VersionMixin, BaseModel):
    python_version: str
    system: str
    release: str
    machine: str
    architecture: Optional[str] = None
    uptime_seconds: Optional[int] = None


class ServiceInfo(BaseModel):
    name: str
    status: str = "running"
    enabled: bool = True


class ServiceRegistryResponse(VersionMixin, BaseModel):
    services: List[ServiceInfo] = Field(default_factory=list)
    total: int = 0


class EngineInfo(BaseModel):
    name: str
    version: str = "V9"
    status: str = "running"


class EngineRegistryResponse(VersionMixin, BaseModel):
    engines: List[EngineInfo] = Field(default_factory=list)
    total: int = 0


class HealthStatusResponse(TimestampMixin, BaseModel):
    healthy: bool
    status: str
    checks: Dict[str, bool] = Field(default_factory=dict)


class RuntimeMetricsResponse(BaseModel):
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    threads: int = 0


class SystemManifestResponse(VersionMixin, BaseModel):
    modules: List[str] = Field(default_factory=list)
    routes: int = 0
    schemas: int = 0
    engines: int = 0
