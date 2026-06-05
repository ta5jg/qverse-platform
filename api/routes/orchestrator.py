from datetime import datetime, timezone

from fastapi import APIRouter
from api.engines.orchestrator_engine import orchestrator_engine

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.get("")
def orchestrator_overview():
    return {
        "platform": "Q-Verse",
        "module": "orchestrator",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overview": orchestrator_engine.overview(),
    }


@router.get("/status")
def orchestrator_status():
    metrics = orchestrator_engine.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "orchestrator_loaded": True,
        "metrics": metrics,
    }


@router.get("/registry")
def orchestrator_registry():
    overview = orchestrator_engine.overview()

    return {
        "components": overview,
        "total": len(overview),
    }


@router.get("/health")
def orchestrator_health():
    return orchestrator_engine.health()