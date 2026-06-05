from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

from api.schemas.enums import ErrorCode
from api.schemas.mixins import TimestampMixin, VersionMixin

T = TypeVar("T")


class APIError(BaseModel):
    code: ErrorCode
    message: str
    field: Optional[str] = None


class ValidationErrorDetail(BaseModel):
    field: str
    message: str


class ResponseMetadata(VersionMixin, BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    trace_id: Optional[str] = None
    execution_time_ms: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Metadata(VersionMixin, BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RequestContext(BaseModel):
    request_id: Optional[str] = None
    trace_id: Optional[str] = None
    actor: Optional[str] = None


class BaseRequest(BaseModel):
    context: Optional[RequestContext] = None


class BaseResponse(VersionMixin, BaseModel):
    success: bool = True
    message: str = "ok"
    metadata: ResponseMetadata = Field(default_factory=ResponseMetadata)


class SuccessResponse(BaseResponse):
    data: Optional[Any] = None


class AsyncOperationResponse(BaseResponse):
    operation_id: str
    state: str = "queued"


class BulkOperationResponse(BaseResponse):
    total: int = 0
    succeeded: int = 0
    failed: int = 0


class ErrorResponse(BaseResponse):
    success: bool = False
    error_code: ErrorCode = ErrorCode.INTERNAL_ERROR
    error: str
    details: Optional[Dict[str, Any]] = None
    errors: List[ValidationErrorDetail] = Field(default_factory=list)


class PaginationRequest(BaseRequest):
    page: int = 1
    page_size: int = 25


class Pagination(BaseModel):
    page: int = 1
    page_size: int = 25
    total_items: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_previous: bool = False


class PaginationResponse(BaseResponse):
    pagination: Pagination


class PaginatedResponse(PaginationResponse, Generic[T]):
    items: List[T] = Field(default_factory=list)


class HealthResponse(TimestampMixin, BaseModel):
    status: str
    service: str


class StatusResponse(TimestampMixin, BaseModel):
    healthy: bool
    status: str
