

#!/usr/bin/env python3
"""Q-Verse V9 Managers Layer Bootstrap Engine.

Creates, repairs and upgrades api/managers/* files.
Protects existing advanced managers unless --force is used.
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

MANAGERS = [
    "system",
    "project",
    "agent",
    "workflow",
    "task",
    "deployment",
    "model",
    "integration",
    "notification",
    "marketplace",
]

PROTECTED_MANAGERS = {
    f"{name}_manager.py" for name in MANAGERS
}

MANAGER_TEMPLATE = '''from __future__ import annotations

from api.services.{service_name}_service import {service_name}_service


class {class_name}:
    def health(self):
        return {{
            "healthy": True,
            "manager": "{manager_name}",
        }}

    def metrics(self):
        return {{
            "manager": "{manager_name}",
            **{service_name}_service.metrics(),
        }}


{manager_name} = {class_name}()
'''


def build_files() -> dict[str, str]:
    files = {}

    exports = []

    for name in MANAGERS:
        class_name = ''.join(part.capitalize() for part in name.split('_')) + 'Manager'

        files[f'api/managers/{name}_manager.py'] = MANAGER_TEMPLATE.format(
            class_name=class_name,
            service_name=name,
            manager_name=f'{name}_manager',
        )

        exports.append(
            f'from api.managers.{name}_manager import {name}_manager, {class_name}'
        )

    files['api/managers/__init__.py'] = (
        '"""Q-Verse Managers Layer V9."""\n\n'
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

    if target.name in PROTECTED_MANAGERS and not force:
        print(f'[PROTECT] {relative_path}')
        return

    if force or should_repair(target):
        target.write_text(content, encoding='utf-8')
        print(f'[REPAIR] {relative_path}')
        return

    print(f'[SKIP] {relative_path}')


def manager_report() -> None:
    manager_dir = ROOT / 'api' / 'managers'
    existing = sorted(p.name for p in manager_dir.glob('*_manager.py'))

    print('\n[REPORT] Managers Layer')
    print(f'[REPORT] Total discovered: {len(existing)}')

    for name in existing:
        print(f'[MANAGER] {name}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    print('Q-Verse V9 Managers Bootstrap Started')

    for path, content in sorted(FILES.items()):
        write_or_repair(path, content, force=args.force)

    manager_report()
    print(f'[SUMMARY] Managed managers: {len(MANAGERS)}')
    print('Q-Verse V9 Managers Bootstrap Complete')


if __name__ == '__main__':
    main()