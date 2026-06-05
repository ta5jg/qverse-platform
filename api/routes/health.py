

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    return {
        "status": "ok",
        "service": "qverse-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready")
def ready():
    return {
        "ready": True,
        "status": "running",
    }


@router.get("/live")
def live():
    return {
        "alive": True,
    }