from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class ModelCapability(BaseModel):
    name: str
    enabled: bool = True
    description: Optional[str] = None


class ModelResponse(VersionMixin, BaseModel):
    model_id: str
    name: str
    provider: str
    version_tag: str
    status: str = "active"
    capabilities: List[ModelCapability] = Field(default_factory=list)


class ModelCreateRequest(BaseModel):
    name: str
    provider: str
    version_tag: str


class ModelUpdateRequest(BaseModel):
    version_tag: Optional[str] = None
    status: Optional[str] = None


class ModelRegistryResponse(VersionMixin, BaseModel):
    models: List[ModelResponse] = Field(default_factory=list)
    total: int = 0


class ModelInferenceRequest(BaseModel):
    model_id: str
    input_text: str
    parameters: Dict[str, str] = Field(default_factory=dict)


class ModelInferenceResponse(TimestampMixin, BaseModel):
    inference_id: str
    model_id: str
    success: bool = True
    output_text: str = ""
    execution_time_ms: float = 0.0


class ModelMetricsResponse(BaseModel):
    total_models: int = 0
    active_models: int = 0
    inference_requests: int = 0
    failed_inferences: int = 0
    average_latency_ms: float = 0.0
    extra: Dict[str, float] = Field(default_factory=dict)


class ModelAuditResponse(BaseModel):
    model_id: str
    event: str
    actor: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModelHealthResponse(TimestampMixin, BaseModel):
    healthy: bool = True
    status: str = "running"
    model_registry_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)
