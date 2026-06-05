from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class VersionMixin(BaseModel):
    version: str = "V9"


class AuditMixin(BaseModel):
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class SoftDeleteMixin(BaseModel):
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
