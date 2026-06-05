#!/usr/bin/env python3
"""
Q-Verse Bootstrap V9
Creates missing schema files and API infrastructure files.
Existing files are never modified.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "api" / "schemas"

SCHEMA_FILES = [
    "common.py",
    "enums.py",
    "mixins.py",
    "system.py",
    "security.py",
    "database.py",
    "projects.py",
    "agents.py",
    "workflows.py",
    "integrations.py",
    "notifications.py",
    "marketplace.py",
    "tasks.py",
    "deployments.py",
    "models.py",
    "audit.py",
    "telemetry.py",
    "logs.py",
    "state.py",
    "config.py",
    "services.py",
    "runtime.py",
    "admin.py",
]

CORE_TEMPLATE_FILES = {
    "enums.py": "# ErrorCode, Role, Permission enums\n",
    "mixins.py": "# TimestampMixin, VersionMixin\n",
    "common.py": "# BaseRequest, BaseResponse, PaginationRequest, PaginationResponse\n",
}

API_STRUCTURE_FILES = [
    "api/core/__init__.py",
    "api/core/config.py",
    "api/core/container.py",
    "api/core/events.py",
    "api/core/exceptions.py",
    "api/core/logging.py",
    "api/core/registry.py",
    "api/core/security.py",
    "api/core/settings.py",
    "api/core/version.py",
    "api/services/__init__.py",
    "api/services/system_service.py",
    "api/services/security_service.py",
    "api/services/database_service.py",
    "api/services/project_service.py",
    "api/services/agent_service.py",
    "api/services/workflow_service.py",
    "api/services/integration_service.py",
    "api/services/notification_service.py",
    "api/services/task_service.py",
    "api/services/deployment_service.py",
    "api/services/audit_service.py",
    "api/services/telemetry_service.py",
    "api/services/model_service.py",
    "api/managers/__init__.py",
    "api/managers/system_manager.py",
    "api/managers/project_manager.py",
    "api/managers/agent_manager.py",
    "api/managers/workflow_manager.py",
    "api/managers/task_manager.py",
    "api/managers/deployment_manager.py",
    "api/managers/model_manager.py",
    "api/managers/integration_manager.py",
    "api/managers/notification_manager.py",
    "api/engines/__init__.py",
    "api/engines/audit_engine.py",
    "api/engines/telemetry_engine.py",
    "api/engines/orchestrator_engine.py",
    "api/engines/runtime_engine.py",
    "api/engines/inference_engine.py",
    "api/repositories/__init__.py",
    "api/repositories/base_repository.py",
    "api/repositories/project_repository.py",
    "api/repositories/task_repository.py",
    "api/repositories/model_repository.py",
    "api/repositories/audit_repository.py",
    "api/dependencies/__init__.py",
    "api/dependencies/auth.py",
    "api/dependencies/database.py",
    "api/dependencies/security.py",
]


def ensure_schemas() -> None:
    SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)

    init_file = SCHEMAS_DIR / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")

    for filename in SCHEMA_FILES:
        target = SCHEMAS_DIR / filename

        if not target.exists():
            target.write_text(
                CORE_TEMPLATE_FILES.get(filename, ""),
                encoding="utf-8",
            )
            print(f"[CREATE] {target}")
        else:
            print(f"[SKIP]   {target}")


def ensure_api_structure() -> None:
    for relative_path in API_STRUCTURE_FILES:
        target = ROOT / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)

        if not target.exists():
            target.write_text("", encoding="utf-8")
            print(f"[CREATE] {target}")
        else:
            print(f"[SKIP]   {target}")


if __name__ == "__main__":
    ensure_schemas()
    ensure_api_structure()
    print("Q-Verse Bootstrap V9 completed")