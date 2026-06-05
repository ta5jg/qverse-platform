

from datetime import datetime, timezone
import os
import platform

from fastapi import APIRouter
from api.engines.runtime_engine import runtime_engine

router = APIRouter(prefix="/runtime", tags=["runtime"])


@router.get("")
def runtime_info():
    return {
        "platform": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "runtime": runtime_engine.status(),
    }


@router.get("/environment")
def environment():
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "qverse_api_port": os.getenv("QVERSE_API_PORT", "8000"),
        "runtime": runtime_engine.get_metrics(),
    }


@router.get("/health")
def runtime_health():
    return runtime_engine.health()


@router.get("/diagnostics")
def runtime_diagnostics():
    return runtime_engine.diagnostics()