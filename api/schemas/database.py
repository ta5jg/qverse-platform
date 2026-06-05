from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from api.schemas.mixins import TimestampMixin, VersionMixin


class DatabaseStatusResponse(TimestampMixin, BaseModel):
    healthy: bool
    status: str
    database_manager_loaded: bool = True
    checks: Dict[str, bool] = Field(default_factory=dict)


class ConnectionPoolResponse(VersionMixin, BaseModel):
    active_connections: int = 0
    idle_connections: int = 0
    pool_size: int = 0
    max_pool_size: int = 0
    pool_available: bool = True


class MigrationResponse(TimestampMixin, BaseModel):
    migration_id: str
    applied: bool
    version: str
    applied_at: Optional[datetime] = None


class MigrationRegistryResponse(VersionMixin, BaseModel):
    migrations: List[MigrationResponse] = Field(default_factory=list)
    total: int = 0


class DatabaseInfoResponse(VersionMixin, BaseModel):
    engine: str = "postgresql"
    host: str
    port: int
    database: str
    schema: str = "public"


class DatabaseMetricsResponse(BaseModel):
    queries_total: int = 0
    transactions_total: int = 0
    failed_queries: int = 0
    average_latency_ms: float = 0.0


class DatabaseHealthResponse(TimestampMixin, BaseModel):
    status: str = "ok"
    database_available: bool = True
    replication_enabled: bool = False


class QueryExecutionResponse(BaseModel):
    query_id: str
    success: bool = True
    execution_time_ms: float = 0.0
