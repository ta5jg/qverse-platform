

#!/usr/bin/env python3
"""Q-Verse V9 Installer Bootstrap + Repair Engine.

This script is designed to be rerunnable and safe by default.

Capabilities:
- Creates missing installer files.
- Fills empty installer files.
- Repairs incomplete generated files.
- Optionally overwrites generated files with --force.
- Produces a clear CREATE / REPAIR / SKIP / UPDATE report.

Scope:
- installer/core/state/platform
- installer/database
- installer/frontend
- installer/integrations
- installer/models
- installer/services
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_FILE_SIZE = 64

FILES: dict[str, str] = {
    "installer/core/state/platform/__init__.py": '''"""Q-Verse Installer Platform Layer V9."""

from installer.core.state.platform.base import PlatformAdapter
from installer.core.state.platform.linux import LinuxPlatformAdapter
from installer.core.state.platform.macos import MacOSPlatformAdapter
from installer.core.state.platform.windows import WindowsPlatformAdapter

__all__ = [
    "PlatformAdapter",
    "LinuxPlatformAdapter",
    "MacOSPlatformAdapter",
    "WindowsPlatformAdapter",
]
''',

    "installer/core/state/platform/base.py": '''from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PlatformAdapter:
    name: str = "generic"

    def detect(self) -> Dict[str, str]:
        return {
            "platform": self.name,
            "status": "detected",
        }

    def validate(self) -> Dict[str, bool]:
        return {
            "supported": True,
            "ready": True,
        }

    def requirements(self) -> list[str]:
        return []
''',

    "installer/core/state/platform/linux.py": '''from __future__ import annotations

from installer.core.state.platform.base import PlatformAdapter


class LinuxPlatformAdapter(PlatformAdapter):
    def __init__(self) -> None:
        super().__init__(name="linux")

    def requirements(self) -> list[str]:
        return ["python3", "nginx", "docker", "postgresql", "redis"]
''',

    "installer/core/state/platform/macos.py": '''from __future__ import annotations

from installer.core.state.platform.base import PlatformAdapter


class MacOSPlatformAdapter(PlatformAdapter):
    def __init__(self) -> None:
        super().__init__(name="macos")

    def requirements(self) -> list[str]:
        return ["python3", "node", "npm"]
''',

    "installer/core/state/platform/windows.py": '''from __future__ import annotations

from installer.core.state.platform.base import PlatformAdapter


class WindowsPlatformAdapter(PlatformAdapter):
    def __init__(self) -> None:
        super().__init__(name="windows")

    def requirements(self) -> list[str]:
        return ["python", "node", "npm"]
''',

    "installer/database/__init__.py": '''"""Q-Verse Installer Database Layer V9."""

from installer.database.schema import DATABASE_SCHEMA
from installer.database.migrations import MigrationPlan
from installer.database.seed import SeedPlan

__all__ = ["DATABASE_SCHEMA", "MigrationPlan", "SeedPlan"]
''',

    "installer/database/schema.py": '''DATABASE_SCHEMA = {
    "version": "V9",
    "tables": [
        "projects",
        "agents",
        "workflows",
        "tasks",
        "models",
        "audit_events",
        "telemetry_events",
    ],
}


def get_schema() -> dict:
    return DATABASE_SCHEMA.copy()
''',

    "installer/database/migrations.py": '''from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MigrationPlan:
    version: str = "V9"
    migrations: list[str] = field(default_factory=list)

    def add(self, migration: str) -> None:
        self.migrations.append(migration)

    def plan(self) -> dict:
        return {
            "version": self.version,
            "migrations": self.migrations,
            "total": len(self.migrations),
        }
''',

    "installer/database/seed.py": '''from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SeedPlan:
    version: str = "V9"
    records: list[dict[str, Any]] = field(default_factory=list)

    def add(self, table: str, data: dict[str, Any]) -> None:
        self.records.append({"table": table, "data": data})

    def plan(self) -> dict:
        return {
            "version": self.version,
            "records": self.records,
            "total": len(self.records),
        }
''',

    "installer/frontend/__init__.py": '''"""Q-Verse Installer Frontend Layer V9."""

from installer.frontend.components import FRONTEND_COMPONENTS
from installer.frontend.nginx_routes import NGINX_ROUTES
from installer.frontend.react_admin import ReactAdminPlan

__all__ = ["FRONTEND_COMPONENTS", "NGINX_ROUTES", "ReactAdminPlan"]
''',

    "installer/frontend/components.py": '''FRONTEND_COMPONENTS = [
    "Dashboard",
    "Projects",
    "Agents",
    "Workflows",
    "Tasks",
    "Models",
    "Telemetry",
    "Audit",
]


def list_components() -> list[str]:
    return FRONTEND_COMPONENTS.copy()
''',

    "installer/frontend/nginx_routes.py": '''NGINX_ROUTES = {
    "/": "frontend",
    "/api": "qverse-api",
    "/admin": "react-admin",
}


def get_nginx_routes() -> dict[str, str]:
    return NGINX_ROUTES.copy()
''',

    "installer/frontend/react_admin.py": '''from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ReactAdminPlan:
    app_name: str = "Q-Verse Admin"
    routes: list[str] = field(default_factory=lambda: [
        "/",
        "/projects",
        "/agents",
        "/workflows",
        "/tasks",
        "/models",
        "/audit",
    ])

    def plan(self) -> dict:
        return {
            "app_name": self.app_name,
            "routes": self.routes,
            "total": len(self.routes),
        }
''',
}

MODEL_PROVIDERS = [
    "anthropic",
    "deepseek",
    "gemini",
    "lmstudio",
    "ollama",
    "openai",
    "openrouter",
]

SERVICE_NAMES = [
    "certbot",
    "docker",
    "nginx",
    "nodejs",
    "postgres",
    "qverse_api",
    "redis",
    "n8n",
]

INTEGRATION_NAMES = [
    "discord",
    "email",
    "signal",
    "slack",
    "telegram",
    "whatsapp",
]


def provider_template(name: str) -> str:
    class_name = ''.join(part.capitalize() for part in name.split('_')) + "Provider"
    return f'''from __future__ import annotations

from dataclasses import dataclass


@dataclass
class {class_name}:
    name: str = "{name}"
    enabled: bool = True

    def status(self) -> dict:
        return {{
            "provider": self.name,
            "enabled": self.enabled,
            "status": "ready",
        }}

    def validate(self) -> dict:
        return {{
            "provider": self.name,
            "valid": True,
        }}


provider = {class_name}()
'''


def service_template(name: str) -> str:
    class_name = ''.join(part.capitalize() for part in name.split('_')) + "InstallerService"
    return f'''from __future__ import annotations

from dataclasses import dataclass


@dataclass
class {class_name}:
    name: str = "{name}"
    enabled: bool = True

    def install_plan(self) -> dict:
        return {{
            "service": self.name,
            "enabled": self.enabled,
            "steps": [
                "validate",
                "install",
                "configure",
                "start",
                "health_check",
            ],
        }}

    def health(self) -> dict:
        return {{
            "service": self.name,
            "healthy": True,
            "status": "ready",
        }}


service = {class_name}()
'''


def integration_template(name: str) -> str:
    class_name = ''.join(part.capitalize() for part in name.split('_')) + "Integration"
    return f'''from __future__ import annotations

from dataclasses import dataclass


@dataclass
class {class_name}:
    name: str = "{name}"
    enabled: bool = True

    def config_schema(self) -> dict:
        return {{
            "integration": self.name,
            "enabled": self.enabled,
            "required_keys": [],
        }}

    def health(self) -> dict:
        return {{
            "integration": self.name,
            "healthy": True,
            "status": "ready",
        }}


integration = {class_name}()
'''


def extend_generated_files() -> None:
    for name in MODEL_PROVIDERS:
        FILES[f"installer/models/{name}.py"] = provider_template(name)

    FILES["installer/models/__init__.py"] = '''"""Q-Verse Installer Model Providers V9."""

MODEL_PROVIDERS = [
    "anthropic",
    "deepseek",
    "gemini",
    "lmstudio",
    "ollama",
    "openai",
    "openrouter",
]


def list_model_providers() -> list[str]:
    return MODEL_PROVIDERS.copy()
'''

    for name in SERVICE_NAMES:
        FILES[f"installer/services/{name}.py"] = service_template(name)

    FILES["installer/services/__init__.py"] = '''"""Q-Verse Installer Services V9."""

INSTALLER_SERVICES = [
    "certbot",
    "docker",
    "nginx",
    "nodejs",
    "postgres",
    "qverse_api",
    "redis",
    "n8n",
]


def list_installer_services() -> list[str]:
    return INSTALLER_SERVICES.copy()
'''

    for name in INTEGRATION_NAMES:
        FILES[f"installer/integrations/{name}.py"] = integration_template(name)

    FILES["installer/integrations/__init__.py"] = '''"""Q-Verse Installer Integrations V9."""

INSTALLER_INTEGRATIONS = [
    "discord",
    "email",
    "signal",
    "slack",
    "telegram",
    "whatsapp",
]


def list_installer_integrations() -> list[str]:
    return INSTALLER_INTEGRATIONS.copy()
'''


def should_repair(target: Path) -> bool:
    if not target.exists():
        return True

    try:
        return target.stat().st_size < MIN_FILE_SIZE
    except OSError:
        return False


def write_or_repair(relative_path: str, content: str, force: bool = False) -> None:
    target = ROOT / relative_path

    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"[CREATE] {relative_path}")
        return

    if force:
        target.write_text(content, encoding="utf-8")
        print(f"[UPDATE] {relative_path}")
        return

    if should_repair(target):
        target.write_text(content, encoding="utf-8")
        print(f"[REPAIR] {relative_path}")
        return

    print(f"[SKIP] {relative_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite generated files")
    args = parser.parse_args()

    extend_generated_files()

    print("Q-Verse V9 Installer Bootstrap Started")

    for path, content in sorted(FILES.items()):
        write_or_repair(path, content, force=args.force)

    print("Q-Verse V9 Installer Bootstrap Complete")


if __name__ == "__main__":
    main()