

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class TelemetryMetric(VersionMixin, BaseModel):
    metric_name: str
    metric_value: float
    unit: Optional[str] = None
    labels: Dict[str, str] = Field(default_factory=dict)


class TelemetryEvent(VersionMixin, BaseModel):
    event_id: str
    event_type: str
    source: str
    payload: Dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TelemetryResponse(VersionMixin, BaseModel):
    metrics_enabled: bool = True
    exporter: str = "internal"
    status: str = "running"


class TelemetryMetricsResponse(VersionMixin, BaseModel):
    metrics: List[TelemetryMetric] = Field(default_factory=list)
    total: int = 0


class TelemetryEventsResponse(VersionMixin, BaseModel):
    events: List[TelemetryEvent] = Field(default_factory=list)
    total: int = 0


class TelemetryExportRequest(BaseModel):
    exporter: str
    destination: Optional[str] = None


class TelemetryExportResponse(TimestampMixin, BaseModel):
    export_id: str
    success: bool = True
    exported_records: int = 0
    execution_time_ms: float = 0.0


class TelemetryMetricsSummary(BaseModel):
    metrics_collected: int = 0
    events_collected: int = 0
    exports_completed: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class TelemetryHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    telemetry_available: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)