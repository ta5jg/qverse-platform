#!/usr/bin/env python3
"""Q-Verse V9 Services Layer Bootstrap Engine.

Creates, repairs and upgrades api/services/* files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_FILE_SIZE = 64
PLACEHOLDER_PATTERNS = [
    "def test_placeholder",
]

AUDIT_PATTERNS = [
    "pass",
    "return {}",
    "def test_placeholder",
]

SERVICE_TEMPLATE = '''from __future__ import annotations

from datetime import datetime, timezone


class {class_name}:
    def health(self):
        return {{
            "healthy": True,
            "service": "{service_name}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }}

    def metrics(self):
        return {{
            "service": "{service_name}",
            "healthy": True,
        }}


{instance_name} = {class_name}()
'''

SERVICES = [
    "health",
    "system",
    "runtime",
    "project",
    "agent",
    "workflow",
    "task",
    "deployment",
    "model",
    "integration",
    "notification",
    "marketplace",
    "audit",
    "backup",
    "telemetry",
    "config",
    "security",
    "database",
]

PROTECTED_SERVICES = {
    "marketplace_service.py",
    "project_service.py",
    "agent_service.py",
    "workflow_service.py",
    "task_service.py",
    "deployment_service.py",
    "model_service.py",
    "integration_service.py",
    "notification_service.py",
    "system_service.py",
    "database_service.py",
    "security_service.py",
    "telemetry_service.py",
    "audit_service.py",
}


def build_files() -> dict[str, str]:
    files: dict[str, str] = {}

    exports = []

    for service in SERVICES:
        class_name = "".join(part.capitalize() for part in service.split("_")) + "Service"
        instance_name = f"{service}_service"

        files[f"api/services/{service}_service.py"] = SERVICE_TEMPLATE.format(
            class_name=class_name,
            service_name=f"{service}_service",
            instance_name=instance_name,
        )

        exports.append(
            f"from api.services.{service}_service import {instance_name}, {class_name}"
        )

    files["api/services/__init__.py"] = (
        '"""Q-Verse Services Layer V9."""\n\n'
        + "\n".join(exports)
        + '\n\n__version__ = "V9"\n'
    )

    return files


FILES = build_files()


def should_repair(target: Path) -> bool:
    if not target.exists():
        return True

    try:
        content = target.read_text(encoding="utf-8")
    except OSError:
        return False

    if target.stat().st_size < MIN_FILE_SIZE:
        return True

    return any(pattern in content for pattern in AUDIT_PATTERNS)


def write_or_repair(relative_path: str, content: str, force: bool = False) -> None:
    target = ROOT / relative_path
    filename = target.name
    target.parent.mkdir(parents=True, exist_ok=True)

    if filename in PROTECTED_SERVICES and not force:
        print(f"[PROTECT] {relative_path}")
        return

    if not target.exists():
        target.write_text(content, encoding="utf-8")
        print(f"[CREATE] {relative_path}")
        return

    if force or should_repair(target):
        target.write_text(content, encoding="utf-8")
        print(f"[REPAIR] {relative_path}")
        return

    print(f"[SKIP] {relative_path}")


def service_report() -> None:
    service_dir = ROOT / "api" / "services"

    existing = sorted(
        p.name for p in service_dir.glob("*_service.py")
    )

    print("\n[REPORT] Services Layer")
    print(f"[REPORT] Total discovered: {len(existing)}")

    for name in existing:
        print(f"[SERVICE] {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    print("Q-Verse V9 Services Bootstrap Started")

    for path, content in sorted(FILES.items()):
        write_or_repair(path, content, force=args.force)

    service_report()

    total_services = len(SERVICES)
    print(f"[SUMMARY] Managed services: {total_services}")

    print("Q-Verse V9 Services Bootstrap Complete")


if __name__ == "__main__":
    main()