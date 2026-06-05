#!/usr/bin/env python3
"""Q-Verse V9 Enterprise Audit Engine.

Audits:
- Python compilation
- Empty files
- Placeholder patterns
- Route inventory
- Test inventory
- Project statistics
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IGNORED_EMPTY_FILES = {
    'api/__init__.py',
    'api/managers/__init__.py',
    'api/middleware/__init__.py',
    'api/models/__init__.py',
    'api/telemetry/__init__.py',
}

SCRIPT_TEMPLATE_FILES = {
    'scripts/audit_project.py',
    'scripts/bootstrap_installer_core.py',
    'scripts/bootstrap_marketplace_and_tests.py',
    'scripts/bootstrap_final_repairs.py',
    'scripts/bootstrap_services_layer.py',
    'scripts/bootstrap_managers_layer.py',
    'scripts/bootstrap_repositories_layer.py',
    'tools/bootstrap_state_engine.py',
}

BOOTSTRAP_PREFIXES = (
    'scripts/bootstrap_',
)


PLACEHOLDER_PATTERNS = [
    '"total": 0',
    'items = []',
    'return {}',
    'pass',
]


class AuditEngine:
    def __init__(self, root: Path):
        self.root = root

    def python_files(self) -> list[Path]:
        return sorted(self.root.rglob('*.py'))

    def empty_files(self) -> list[str]:
        result = []
        for file in self.python_files():
            try:
                rel = str(file.relative_to(self.root))
                if rel in IGNORED_EMPTY_FILES:
                    continue

                if file.stat().st_size == 0:
                    result.append(rel)
            except OSError:
                continue
        return result

    def placeholder_files(self) -> dict[str, list[str]]:
        findings: dict[str, list[str]] = {}

        for file in self.python_files():
            rel = str(file.relative_to(self.root))

            if rel in SCRIPT_TEMPLATE_FILES:
                continue

            if rel.startswith(BOOTSTRAP_PREFIXES):
                continue

            try:
                content = file.read_text(encoding='utf-8')
            except Exception:
                continue

            matches = [p for p in PLACEHOLDER_PATTERNS if p in content]
            if matches:
                findings[rel] = matches

        return findings

    def compile_audit(self) -> bool:
        try:
            subprocess.run(
                ['python3', '-m', 'py_compile', *[str(f) for f in self.python_files()]],
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def route_count(self) -> int:
        route_dir = self.root / 'api' / 'routes'
        return len(list(route_dir.glob('*.py'))) if route_dir.exists() else 0

    def test_count(self) -> int:
        test_dir = self.root / 'tests'
        return len(list(test_dir.rglob('test_*.py'))) if test_dir.exists() else 0

    def marketplace_status(self) -> str:
        required_files = [
            self.root / 'api' / 'routes' / 'marketplace.py',
            self.root / 'api' / 'managers' / 'marketplace_manager.py',
            self.root / 'api' / 'services' / 'marketplace_service.py',
            self.root / 'api' / 'repositories' / 'marketplace_repository.py',
            self.root / 'api' / 'schemas' / 'marketplace.py',
        ]

        if not all(path.exists() and path.stat().st_size > 0 for path in required_files):
            return 'needs_manager_integration'

        route_file = self.root / 'api' / 'routes' / 'marketplace.py'
        content = route_file.read_text(encoding='utf-8')

        if 'from api.managers.marketplace_manager import marketplace_manager' not in content:
            return 'needs_manager_integration'

        if 'marketplace_manager.get_dashboard()' not in content:
            return 'needs_manager_integration'

        if 'marketplace_manager.list_items()' not in content:
            return 'needs_manager_integration'

        if 'api/routes/marketplace.py' in self.placeholder_files():
            return 'needs_manager_integration'

        return 'integrated'

    def real_missing_or_incomplete(self) -> list[str]:
        findings: list[str] = []

        findings.extend(self.empty_files())

        for path in self.placeholder_files().keys():
            findings.append(path)

        return sorted(set(findings))

    def report(self) -> dict:
        return {
            'project': 'Q-Verse',
            'audit_version': 'V9',
            'python_files': len(self.python_files()),
            'routes': self.route_count(),
            'tests': self.test_count(),
            'compile_ok': self.compile_audit(),
            'empty_files': self.empty_files(),
            'placeholder_files': self.placeholder_files(),
            'real_missing_or_incomplete': self.real_missing_or_incomplete(),
            'marketplace_status': self.marketplace_status(),
        }


if __name__ == '__main__':
    engine = AuditEngine(ROOT)
    print(json.dumps(engine.report(), indent=2))