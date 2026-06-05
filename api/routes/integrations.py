from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.integration_manager import integration_manager

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("")
def integrations_overview():
    return {
        "platform": "Q-Verse",
        "module": "integrations",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": integration_manager.get_dashboard(),
    }


@router.get("/status")
def integrations_status():
    metrics = integration_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "integration_manager_loaded": True,
        "metrics": metrics,
    }


@router.get("/registry")
def integrations_registry():
    integrations = integration_manager.list_integrations()

    return {
        "integrations": integrations,
        "total": len(integrations),
    }


@router.get("/health")
def integrations_health():
    metrics = integration_manager.get_metrics()

    return {
        "status": "ok",
        "integrations_available": True,
        "metrics": metrics,
    }