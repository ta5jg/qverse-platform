

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class LogEntry(VersionMixin, BaseModel):
    log_id: str
    level: str
    message: str
    source: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, str] = Field(default_factory=dict)


class LogQueryRequest(BaseModel):
    level: Optional[str] = None
    source: Optional[str] = None
    limit: int = 100


class LogRegistryResponse(VersionMixin, BaseModel):
    entries: List[LogEntry] = Field(default_factory=list)
    total: int = 0


class LogExportRequest(BaseModel):
    format: str = "json"
    destination: Optional[str] = None


class LogExportResponse(TimestampMixin, BaseModel):
    export_id: str
    success: bool = True
    exported_records: int = 0
    execution_time_ms: float = 0.0


class LogMetricsResponse(BaseModel):
    total_logs: int = 0
    info_logs: int = 0
    warning_logs: int = 0
    error_logs: int = 0
    critical_logs: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class LogAuditResponse(BaseModel):
    log_id: str
    action: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LogHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    logging_available: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)