

#!/usr/bin/env python3
"""Q-Verse Platform V9 Master Bootstrap.

Runs all bootstrap engines, validates project state,
and provides a consolidated report.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BOOTSTRAPS = [
    "scripts/bootstrap_installer.py",
    "scripts/bootstrap_installer_core.py",
    "scripts/bootstrap_marketplace_and_tests.py",
    "scripts/bootstrap_final_repairs.py",
    "scripts/bootstrap_services_layer.py",
    "scripts/bootstrap_managers_layer.py",
    "scripts/bootstrap_repositories_layer.py",
    "scripts/bootstrap_schemas_layer.py",
    "scripts/bootstrap_tests_layer.py",
    "scripts/bootstrap_frontend_layer.py",
    "scripts/bootstrap_frontend_repairs.py",
]

AUDITS = [
    "scripts/audit_project.py",
    "scripts/bootstrap_frontend_audit.py",
]


def run_script(script: str, force: bool = False) -> bool:
    target = ROOT / script

    if not target.exists():
        print(f"[MISSING] {script}")
        return False

    cmd = [sys.executable, str(target)]

    if force:
        cmd.append("--force")

    print(f"\n[RUN] {script}")

    result = subprocess.run(cmd, cwd=ROOT)

    if result.returncode == 0:
        print(f"[OK] {script}")
        return True

    print(f"[FAIL] {script}")
    return False



def compile_project() -> bool:
    py_files = list(ROOT.rglob("*.py"))

    for file in py_files:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file)],
            cwd=ROOT,
            capture_output=True,
        )

        if result.returncode != 0:
            print(f"[COMPILE_FAIL] {file}")
            return False

    return True



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    print("=" * 60)
    print("Q-VERSE PLATFORM V9 MASTER BOOTSTRAP")
    print("=" * 60)

    success = 0

    for script in BOOTSTRAPS:
        if run_script(script, args.force):
            success += 1

    print("\n[STAGE] Compile Validation")

    compile_ok = compile_project()

    print(f"[COMPILE] {'OK' if compile_ok else 'FAILED'}")

    print("\n[STAGE] Audits")

    for script in AUDITS:
        run_script(script, False)

    print("\n" + "=" * 60)
    print("Q-VERSE V9 SUMMARY")
    print("=" * 60)
    print(f"Bootstrap Scripts : {len(BOOTSTRAPS)}")
    print(f"Successful Runs   : {success}")
    print(f"Compile Status    : {'PASS' if compile_ok else 'FAIL'}")
    print("Audit Status      : EXECUTED")
    print("Platform State    : V9 ENTERPRISE")
    print("=" * 60)


if __name__ == "__main__":
    main()