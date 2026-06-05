from datetime import datetime, timezone

from fastapi import APIRouter
from api.managers.model_manager import model_manager

router = APIRouter(prefix="/models", tags=["models"])


@router.get("")
def models_overview():
    return {
        "platform": "Q-Verse",
        "module": "models",
        "version": "V9",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dashboard": model_manager.get_dashboard(),
    }


@router.get("/status")
def models_status():
    metrics = model_manager.get_metrics()

    return {
        "healthy": True,
        "status": "running",
        "model_registry_loaded": True,
        "metrics": metrics,
    }


@router.get("/registry")
def models_registry():
    models = model_manager.list_models()

    return {
        "models": models,
        "total": len(models),
    }


@router.get("/health")
def models_health():
    metrics = model_manager.get_metrics()

    return {
        "status": "ok",
        "models_available": True,
        "metrics": metrics,
    }
