

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class NotificationResponse(VersionMixin, BaseModel):
    notification_id: str
    title: str
    message: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NotificationCreateRequest(BaseModel):
    title: str
    message: str
    channel: str


class NotificationUpdateRequest(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None


class NotificationQueueResponse(VersionMixin, BaseModel):
    pending_notifications: int = 0
    delivery_enabled: bool = True
    queue_size: int = 0


class NotificationDeliveryResponse(TimestampMixin, BaseModel):
    delivery_id: str
    notification_id: str
    success: bool = True
    delivered_at: Optional[datetime] = None
    execution_time_ms: float = 0.0


class NotificationSubscriptionResponse(VersionMixin, BaseModel):
    subscriber_id: str
    channel: str
    enabled: bool = True


class NotificationRegistryResponse(VersionMixin, BaseModel):
    notifications: List[NotificationResponse] = Field(default_factory=list)
    total: int = 0


class NotificationMetricsResponse(BaseModel):
    total_notifications: int = 0
    delivered_notifications: int = 0
    failed_notifications: int = 0
    queued_notifications: int = 0
    extra: Dict[str, int] = Field(default_factory=dict)


class NotificationAuditResponse(BaseModel):
    notification_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class NotificationHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    notification_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)