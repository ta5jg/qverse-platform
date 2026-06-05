from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.deployment_manager import deployment_manager

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.get("")
def deployments_overview():
    return {
        "platform": "Q-Verse",
        "module": "deployments",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": deployment_manager.get_dashboard(),
    }


@router.get("/status")
def deployments_status():
    metrics = deployment_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "deployment_manager_loaded": True,
        "metrics": metrics,
    }


@router.get("/registry")
def deployments_registry():
    deployments = deployment_manager.list_deployments()

    return {
        "deployments": deployments,
        "total": len(deployments),
    }


@router.get("/health")
def deployments_health():
    metrics = deployment_manager.get_metrics()

    return {
        "status": "ok",
        "deployments_available": True,
        "metrics": metrics,
    }