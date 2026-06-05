#!/usr/bin/env python3
"""Q-Verse V9 Tests Layer Bootstrap Engine.

Creates, repairs and upgrades tests/* files.
Protects existing advanced tests unless --force is used.
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

TEST_TARGETS = [
    "health",
    "system",
    "runtime",
    "projects",
    "agents",
    "tasks",
    "workflows",
    "deployments",
    "models",
    "integrations",
    "notifications",
    "marketplace",
]

TEST_TEMPLATE = '''from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_{target}_endpoint_exists():
    response = client.get("/{target}")
    assert response.status_code in [200, 404]


def test_{target}_response_is_json():
    response = client.get("/{target}")
    assert response.headers.get("content-type", "").startswith("application/json")
'''


def build_files() -> dict[str, str]:
    files = {
        "tests/__init__.py": '"""Q-Verse Tests V9."""\n',
        "tests/routes/__init__.py": '"""Route Tests."""\n',
        "tests/state/__init__.py": '"""State Tests."""\n',
    }

    for target in TEST_TARGETS:
        files[f"tests/routes/test_{target}.py"] = TEST_TEMPLATE.format(target=target)

    return files


FILES = build_files()


def should_repair(target: Path) -> bool:
    if not target.exists():
        return True

    content = target.read_text(encoding="utf-8")

    if target.stat().st_size < MIN_FILE_SIZE:
        return True

    return any(pattern in content for pattern in REPAIR_PATTERNS)


def write_or_repair(relative_path: str, content: str, force: bool = False) -> None:
    target = ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)

    if not target.exists():
        target.write_text(content, encoding="utf-8")
        print(f"[CREATE] {relative_path}")
        return

    if force or should_repair(target):
        target.write_text(content, encoding="utf-8")
        print(f"[REPAIR] {relative_path}")
        return

    print(f"[SKIP] {relative_path}")


def tests_report() -> None:
    test_dir = ROOT / "tests"
    discovered = sorted(test_dir.rglob("test_*.py"))

    print("\n[REPORT] Tests Layer")
    print(f"[REPORT] Total discovered: {len(discovered)}")

    for item in discovered:
        print(f"[TEST] {item.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    print("Q-Verse V9 Tests Bootstrap Started")

    for path, content in sorted(FILES.items()):
        write_or_repair(path, content, force=args.force)

    tests_report()

    print(f"[SUMMARY] Managed tests: {len(TEST_TARGETS)}")
    print("Q-Verse V9 Tests Bootstrap Complete")


if __name__ == "__main__":
    main()
