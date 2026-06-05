

#!/usr/bin/env python3
"""Q-Verse V9 Schemas Layer Bootstrap Engine.

Creates, repairs and upgrades api/schemas/* files.
Protects existing advanced schemas unless --force is used.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_FILE_SIZE = 64

REPAIR_PATTERNS = [
    "pass",
    "return {}",
    "def test_placeholder",
]

SCHEMAS = [
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
    "security",
]

PROTECTED_SCHEMAS = {f"{name}.py" for name in SCHEMAS}

SCHEMA_TEMPLATE = '''from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from pydantic import BaseModel, Field


class {class_name}(BaseModel):
    id: str
    name: str
    status: str = "active"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class {class_name}Response(BaseModel):
    healthy: bool = True
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
'''


def build_files() -> dict[str, str]:
    files = {}
    exports = []

    for name in SCHEMAS:
        class_name = ''.join(part.capitalize() for part in name.split('_'))

        files[f'api/schemas/{name}.py'] = SCHEMA_TEMPLATE.format(
            class_name=class_name,
        )

        exports.append(
            f'from api.schemas.{name} import {class_name}, {class_name}Response'
        )

    files['api/schemas/__init__.py'] = (
        '"""Q-Verse Schemas Layer V9."""\n\n'
        + '\n'.join(exports)
        + '\n\n__version__ = "V9"\n'
    )

    return files


FILES = build_files()


def should_repair(target: Path) -> bool:
    if not target.exists():
        return True

    content = target.read_text(encoding='utf-8')

    if target.stat().st_size < MIN_FILE_SIZE:
        return True

    return any(pattern in content for pattern in REPAIR_PATTERNS)


def write_or_repair(relative_path: str, content: str, force: bool = False) -> None:
    target = ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)

    if not target.exists():
        target.write_text(content, encoding='utf-8')
        print(f'[CREATE] {relative_path}')
        return

    if target.name in PROTECTED_SCHEMAS and not force:
        print(f'[PROTECT] {relative_path}')
        return

    if force or should_repair(target):
        target.write_text(content, encoding='utf-8')
        print(f'[REPAIR] {relative_path}')
        return

    print(f'[SKIP] {relative_path}')


def schema_report() -> None:
    schema_dir = ROOT / 'api' / 'schemas'
    existing = sorted(p.name for p in schema_dir.glob('*.py'))

    print('\n[REPORT] Schemas Layer')
    print(f'[REPORT] Total discovered: {len(existing)}')

    for name in existing:
        print(f'[SCHEMA] {name}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    print('Q-Verse V9 Schemas Bootstrap Started')

    for path, content in sorted(FILES.items()):
        write_or_repair(path, content, force=args.force)

    schema_report()
    print(f'[SUMMARY] Managed schemas: {len(SCHEMAS)}')
    print('Q-Verse V9 Schemas Bootstrap Complete')


if __name__ == '__main__':
    main()