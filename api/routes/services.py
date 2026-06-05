

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/services", tags=["services"])


@router.get("")
def services_overview():
    return {
        "platform": "Q-Verse",
        "services": [
            "api",
            "postgres",
            "redis",
            "backup",
            "audit",
            "logger",
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/status")
def services_status():
    return {
        "healthy": True,
        "status": "running",
    }


@router.get("/registry")
def services_registry():
    return {
        "registered": [
            "health",
            "system",
            "runtime",
            "services",
        ]
    }