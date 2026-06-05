from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.agent_manager import agent_manager

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def agents_overview():
    return {
        "platform": "Q-Verse",
        "module": "agents",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": agent_manager.get_dashboard(),
    }


@router.get("/status")
def agents_status():
    metrics = agent_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "agent_manager_loaded": True,
        "metrics": metrics,
    }


@router.get("/registry")
def agents_registry():
    agents = agent_manager.list_agents()

    return {
        "agents": agents,
        "total": len(agents),
    }


@router.get("/health")
def agents_health():
    metrics = agent_manager.get_metrics()

    return {
        "status": "ok",
        "agents_available": True,
        "metrics": metrics,
    }