from fastapi import APIRouter
from api.managers.system_manager import system_manager

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.get("")
def get_orchestrator_metrics():
    return system_manager.get_metrics()


@router.get("/")
def get_orchestrator_metrics_slash():
    return system_manager.get_metrics()
