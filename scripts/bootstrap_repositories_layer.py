

#!/usr/bin/env python3
"""Q-Verse V9 Repositories Layer Bootstrap Engine.

Creates, repairs and upgrades api/repositories/* files.
Protects existing advanced repositories unless --force is used.
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

REPOSITORIES = [
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
]

PROTECTED_REPOSITORIES = {
    f"{name}_repository.py" for name in REPOSITORIES
}

REPOSITORY_TEMPLATE = '''from __future__ import annotations

from typing import Any, Dict, List, Optional

from api.repositories.base_repository import BaseRepository


class {class_name}(BaseRepository[Dict[str, Any]]):
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for item in self.list_all():
            if item.get("name") == name:
                return item
        return None

    def metrics(self) -> Dict[str, Any]:
        return {{
            "repository": "{repository_name}",
            "total_records": self.count(),
        }}


{repository_name} = {class_name}()
'''


def build_files() -> dict[str, str]:
    files = {}
    exports = []

    for name in REPOSITORIES:
        class_name = ''.join(part.capitalize() for part in name.split('_')) + 'Repository'
        repository_name = f'{name}_repository'

        files[f'api/repositories/{name}_repository.py'] = REPOSITORY_TEMPLATE.format(
            class_name=class_name,
            repository_name=repository_name,
        )

        exports.append(
            f'from api.repositories.{name}_repository import {repository_name}, {class_name}'
        )

    files['api/repositories/__init__.py'] = (
        '"""Q-Verse Repositories Layer V9."""\n\n'
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

    if target.name in PROTECTED_REPOSITORIES and not force:
        print(f'[PROTECT] {relative_path}')
        return

    if force or should_repair(target):
        target.write_text(content, encoding='utf-8')
        print(f'[REPAIR] {relative_path}')
        return

    print(f'[SKIP] {relative_path}')


def repository_report() -> None:
    repository_dir = ROOT / 'api' / 'repositories'
    existing = sorted(p.name for p in repository_dir.glob('*_repository.py'))

    print('\n[REPORT] Repositories Layer')
    print(f'[REPORT] Total discovered: {len(existing)}')

    for name in existing:
        print(f'[REPOSITORY] {name}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    print('Q-Verse V9 Repositories Bootstrap Started')

    for path, content in sorted(FILES.items()):
        write_or_repair(path, content, force=args.force)

    repository_report()
    print(f'[SUMMARY] Managed repositories: {len(REPOSITORIES)}')
    print('Q-Verse V9 Repositories Bootstrap Complete')


if __name__ == '__main__':
    main()