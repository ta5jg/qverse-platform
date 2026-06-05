

from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.workflow_manager import workflow_manager

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("")
def workflows_overview():
    return {
        "platform": "Q-Verse",
        "module": "workflows",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": workflow_manager.get_dashboard(),
    }


@router.get("/status")
def workflows_status():
    metrics = workflow_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "workflow_manager_loaded": True,
        "metrics": metrics,
    }


@router.get("/registry")
def workflows_registry():
    workflows = workflow_manager.list_workflows()

    return {
        "workflows": workflows,
        "total": len(workflows),
    }


@router.get("/health")
def workflows_health():
    metrics = workflow_manager.get_metrics()

    return {
        "status": "ok",
        "workflows_available": True,
        "metrics": metrics,
    }