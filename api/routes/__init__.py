"""
Q-Verse API Routes Registry V9 Enterprise
"""

from dataclasses import dataclass
from typing import List

from fastapi import APIRouter

from api.routes.admin import router as admin_router
from api.routes.agents import router as agents_router
from api.routes.audit import router as audit_router
from api.routes.backup import router as backup_router
from api.routes.config import router as config_router
from api.routes.database import router as database_router
from api.routes.deployments import router as deployments_router
from api.routes.engines import router as engines_router
from api.routes.health import router as health_router
from api.routes.integrations import router as integrations_router
from api.routes.logs import router as logs_router
from api.routes.marketplace import router as marketplace_router
from api.routes.models import router as models_router
from api.routes.notifications import router as notifications_router
from api.routes.orchestrator import router as orchestrator_router
from api.routes.projects import router as projects_router
from api.routes.runtime import router as runtime_router
from api.routes.security import router as security_router
from api.routes.services import router as services_router
from api.routes.state import router as state_router
from api.routes.system import router as system_router
from api.routes.tasks import router as tasks_router
from api.routes.telemetry import router as telemetry_router
from api.routes.workflows import router as workflows_router
from api.routes.agent_chat import router as agent_chat_router

ROUTES_VERSION = "V9"
ROUTES_STATUS = "V9_ENTERPRISE_COMPLETE"


@dataclass(frozen=True)
class RouteDefinition:
    name: str
    prefix: str
    router: APIRouter
    version: str = ROUTES_VERSION
    enabled: bool = True


ROUTE_REGISTRY: List[RouteDefinition] = [
    RouteDefinition("health", "/health", health_router),
    RouteDefinition("system", "/system", system_router),
    RouteDefinition("runtime", "/runtime", runtime_router),
    RouteDefinition("services", "/services", services_router),
    RouteDefinition("engines", "/engines", engines_router),
    RouteDefinition("admin", "/admin", admin_router),
    RouteDefinition("telemetry", "/telemetry", telemetry_router),
    RouteDefinition("config", "/config", config_router),
    RouteDefinition("audit", "/audit", audit_router),
    RouteDefinition("backup", "/backup", backup_router),
    RouteDefinition("logs", "/logs", logs_router),
    RouteDefinition("state", "/state", state_router),
    RouteDefinition("projects", "/projects", projects_router),
    RouteDefinition("models", "/models", models_router),
    RouteDefinition("integrations", "/integrations", integrations_router),
    RouteDefinition("database", "/database", database_router),
    RouteDefinition("security", "/security", security_router),
    RouteDefinition("tasks", "/tasks", tasks_router),
    RouteDefinition("notifications", "/notifications", notifications_router),
    RouteDefinition("agents", "/agents", agents_router),
    RouteDefinition("orchestrator", "/orchestrator", orchestrator_router),
    RouteDefinition("deployments", "/deployments", deployments_router),
    RouteDefinition("workflows", "/workflows", workflows_router),
    RouteDefinition("marketplace", "/marketplace", marketplace_router),
]


def enabled_routers() -> List[APIRouter]:
    return [route.router for route in ROUTE_REGISTRY if route.enabled]


def route_manifest() -> dict:
    enabled_routes = [route for route in ROUTE_REGISTRY if route.enabled]
    return {
        "version": ROUTES_VERSION,
        "status": ROUTES_STATUS,
        "total": len(ROUTE_REGISTRY),
        "enabled": len(enabled_routes),
        "routes": [
            {
                "name": route.name,
                "prefix": route.prefix,
                "version": route.version,
                "enabled": route.enabled,
            }
            for route in ROUTE_REGISTRY
        ],
    }
