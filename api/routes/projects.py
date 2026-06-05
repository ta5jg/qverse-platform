from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.project_manager import project_manager

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def projects_overview():
    return {
        "platform": "Q-Verse",
        "module": "projects",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": project_manager.get_dashboard(),
    }


@router.get("/status")
def projects_status():
    metrics = project_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "project_manager_loaded": True,
        "metrics": metrics,
    }


@router.get("/registry")
def projects_registry():
    projects = project_manager.list_projects()

    return {
        "projects": projects,
        "total": len(projects),
    }


@router.get("/health")
def projects_health():
    metrics = project_manager.get_metrics()

    return {
        "status": "ok",
        "projects_available": True,
        "metrics": metrics,
    }
