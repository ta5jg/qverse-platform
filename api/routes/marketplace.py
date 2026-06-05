from datetime import datetime, timezone

from fastapi import APIRouter

from api.managers.marketplace_manager import marketplace_manager

router = APIRouter(prefix="/marketplace", tags=["marketplace"])


@router.get("")
def marketplace_overview():
    dashboard = marketplace_manager.get_dashboard()

    return {
        "platform": "Q-Verse",
        "module": "marketplace",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "catalog": dashboard,
        "metrics": marketplace_manager.get_metrics(),
    }


@router.get("/status")
def marketplace_status():
    return {
        "healthy": True,
        "status": "running",
        "marketplace_loaded": True,
        "catalog_enabled": True,
        "metrics": marketplace_manager.get_metrics(),
    }


@router.get("/registry")
def marketplace_registry():
    items = marketplace_manager.list_items()

    return {
        "items": items,
        "total": len(items),
    }


@router.get("/health")
def marketplace_health():
    return {
        "status": "ok",
        "marketplace_available": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": marketplace_manager.get_metrics(),
    }
