from datetime import datetime, timezone
import platform

from fastapi import APIRouter
from api.managers.system_manager import system_manager

router = APIRouter(prefix="/system", tags=["system"])


@router.get("")
def system_info():
    return {
        "platform": "Q-Verse",
        "version": "4.0.0",
        "api": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": system_manager.get_metrics(),
    }


@router.get("/runtime")
def runtime():
    return {
        "python_version": platform.python_version(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "diagnostics": system_manager.diagnostics(),
    }


@router.get("/status")
def status():
    return {
        "status": "running",
        "healthy": True,
        "metrics": system_manager.get_metrics(),
    }
