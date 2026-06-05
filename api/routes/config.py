from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/config", tags=["config"])


@router.get("")
def config_overview():
    return {
        "platform": "Q-Verse",
        "module": "config",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/status")
def config_status():
    return {
        "healthy": True,
        "status": "running",
        "config_loaded": True,
    }


@router.get("/schema")
def config_schema():
    return {
        "supported": [
            "yaml",
            "json",
            "env",
        ]
    }


@router.get("/health")
def config_health():
    return {
        "status": "ok",
        "config_available": True,
    }
