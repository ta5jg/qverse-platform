from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.notification_manager import notification_manager

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def notifications_overview():
    return {
        "platform": "Q-Verse",
        "module": "notifications",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": notification_manager.get_dashboard(),
    }


@router.get("/status")
def notifications_status():
    metrics = notification_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "notification_manager_loaded": True,
        "metrics": metrics,
    }


@router.get("/queue")
def notifications_queue():
    notifications = notification_manager.list_notifications()

    return {
        "notifications": notifications,
        "total": len(notifications),
    }


@router.get("/health")
def notifications_health():
    metrics = notification_manager.get_metrics()

    return {
        "status": "ok",
        "notifications_available": True,
        "metrics": metrics,
    }
