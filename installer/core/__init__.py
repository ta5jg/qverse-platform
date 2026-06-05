

"""
Q-Verse Core Runtime V9

Purpose:
    Central registry and lifecycle entry point for Q-Verse core engines.

Core Engines:
    State Engine
    Config Engine
    Audit Engine
    Backup Engine
    Logger Engine
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Type

from .config import ConfigManager, CONFIG_ENGINE_VERSION
from .audit import AuditEngine, AUDIT_ENGINE_VERSION
from .backup import BackupEngine, BACKUP_ENGINE_VERSION, BACKUP_ENGINE_STATUS
from .logger import LoggerEngine, LOGGER_ENGINE_VERSION, LOGGER_ENGINE_STATUS

__version__ = "4.0.0"
__platform__ = "Q-Verse"
CORE_RUNTIME_STATUS = "V9_ENTERPRISE_COMPLETE"


@dataclass
class EngineMetadata:
    name: str
    version: str
    status: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)


@dataclass
class EngineHealth:
    name: str
    available: bool
    status: str
    version: str
    errors: List[str] = field(default_factory=list)


CORE_ENGINES: Dict[str, Type[Any]] = {
    "config": ConfigManager,
    "audit": AuditEngine,
    "backup": BackupEngine,
    "logger": LoggerEngine,
}


ENGINE_METADATA: Dict[str, EngineMetadata] = {
    "config": EngineMetadata(
        name="config",
        version=CONFIG_ENGINE_VERSION,
        status="stable",
        description="Desired state and configuration engine",
        dependencies=[],
        capabilities=[
            "yaml_loading",
            "desired_state",
            "validation",
            "dependency_validation",
            "config_diff",
            "config_export",
            "checksum",
        ],
    ),
    "audit": EngineMetadata(
        name="audit",
        version=AUDIT_ENGINE_VERSION,
        status="stable",
        description="Current state versus desired state analyzer",
        dependencies=["config"],
        capabilities=[
            "service_audit",
            "security_audit",
            "database_audit",
            "risk_analysis",
            "compliance_scoring",
            "action_planning",
            "report_export",
        ],
    ),
    "backup": EngineMetadata(
        name="backup",
        version=BACKUP_ENGINE_VERSION,
        status=BACKUP_ENGINE_STATUS,
        description="Recovery and protection engine",
        dependencies=["logger"],
        capabilities=[
            "archive_backup",
            "checksum_verification",
            "restore",
            "retention_policy",
            "disaster_recovery",
            "aes256_encryption",
            "s3_upload",
            "minio_upload",
            "postgres_dump",
            "redis_snapshot",
            "scheduler_definition",
        ],
    ),
    "logger": EngineMetadata(
        name="logger",
        version=LOGGER_ENGINE_VERSION,
        status=LOGGER_ENGINE_STATUS,
        description="Central observability and execution tracking engine",
        dependencies=[],
        capabilities=[
            "event_logging",
            "audit_trail",
            "security_events",
            "metrics",
            "alerts",
            "log_rotation",
            "retention",
            "prometheus_export",
            "opentelemetry_hook",
            "remote_sink",
        ],
    ),
}


def list_engines() -> List[str]:
    return sorted(CORE_ENGINES.keys())


def get_engine(name: str):
    return CORE_ENGINES.get(name)


def create_engine(name: str, *args, **kwargs):
    engine = get_engine(name)

    if not engine:
        raise KeyError(f"Unknown Q-Verse engine: {name}")

    return engine(*args, **kwargs)


def get_engine_metadata(name: str) -> Optional[EngineMetadata]:
    return ENGINE_METADATA.get(name)


def engine_versions() -> Dict[str, str]:
    return {
        name: metadata.version
        for name, metadata in ENGINE_METADATA.items()
    }


def engine_capabilities() -> Dict[str, List[str]]:
    return {
        name: metadata.capabilities
        for name, metadata in ENGINE_METADATA.items()
    }


def engine_dependencies() -> Dict[str, List[str]]:
    return {
        name: metadata.dependencies
        for name, metadata in ENGINE_METADATA.items()
    }


def engine_health() -> Dict[str, Dict[str, Any]]:
    health = {}

    for name, engine_cls in CORE_ENGINES.items():
        metadata = ENGINE_METADATA.get(name)
        errors = []
        available = True

        try:
            engine_cls
        except Exception as exc:
            available = False
            errors.append(str(exc))

        result = EngineHealth(
            name=name,
            available=available,
            status=metadata.status if metadata else "unknown",
            version=metadata.version if metadata else "unknown",
            errors=errors,
        )
        health[name] = asdict(result)

    return health


def runtime_report() -> Dict[str, Any]:
    return {
        "platform": __platform__,
        "version": __version__,
        "status": CORE_RUNTIME_STATUS,
        "engines": list_engines(),
        "versions": engine_versions(),
        "dependencies": engine_dependencies(),
        "capabilities": engine_capabilities(),
        "health": engine_health(),
    }


__all__ = [
    "ConfigManager",
    "AuditEngine",
    "BackupEngine",
    "LoggerEngine",
    "EngineMetadata",
    "EngineHealth",
    "CORE_ENGINES",
    "ENGINE_METADATA",
    "CORE_RUNTIME_STATUS",
    "get_engine",
    "create_engine",
    "get_engine_metadata",
    "list_engines",
    "engine_versions",
    "engine_capabilities",
    "engine_dependencies",
    "engine_health",
    "runtime_report",
]