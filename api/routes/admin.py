

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("")
def admin_overview():
    return {
        "platform": "Q-Verse",
        "module": "admin",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/status")
def admin_status():
    return {
        "healthy": True,
        "status": "running",
        "admin_enabled": True,
    }


@router.get("/permissions")
def admin_permissions():
    return {
        "roles": [
            "admin",
            "operator",
            "auditor",
        ]
    }


@router.get("/health")
def admin_health():
    return {
        "status": "ok",
        "admin_available": True,
    }