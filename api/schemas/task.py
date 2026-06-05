from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    name: str
    status: str = "active"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    healthy: bool = True
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
