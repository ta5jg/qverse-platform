

from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.task_manager import task_manager

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
def tasks_overview():
    return {
        "platform": "Q-Verse",
        "module": "tasks",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": task_manager.get_dashboard(),
    }


@router.get("/status")
def tasks_status():
    metrics = task_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "task_manager_loaded": True,
        "metrics": metrics,
    }


@router.get("/queue")
def tasks_queue():
    tasks = task_manager.list_tasks()

    return {
        "tasks": tasks,
        "total": len(tasks),
    }


@router.get("/health")
def tasks_health():
    metrics = task_manager.get_metrics()

    return {
        "status": "ok",
        "tasks_available": True,
        "metrics": metrics,
    }