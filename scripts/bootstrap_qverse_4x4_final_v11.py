#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BOOTSTRAPS = [
    "scripts/bootstrap_api_runtime_fix.py",
    "scripts/bootstrap_clients_v9.py",
    "scripts/bootstrap_ai_live_transport.py",
    "scripts/bootstrap_ai_transport_v102.py",
    "scripts/bootstrap_provider_pack_v103.py",
    "scripts/bootstrap_multi_provider_runtime_v104.py",
]

def run_script(script_path, force=False):
    path = ROOT / script_path
    if not path.exists():
        print(f"[SKIP] {script_path} (not found)")
        return False
    cmd = ["python3", str(path)]
    if force:
        cmd.append("--force")
    print(f"[RUN] {script_path}")
    try:
        subprocess.run(cmd, check=True)
        print(f"[OK] {script_path}")
        return True
    except subprocess.CalledProcessError:
        print(f"[FAIL] {script_path}")
        return False

def generate_final_report(results):
    report_path = ROOT / "reports" / "qverse_4x4_final_v11.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    executed = len(results)
    successful = sum(results)
    content = {
        "version": "V11",
        "status": "bootstrap_complete",
        "executed": executed,
        "successful": successful,
    }
    import json
    with report_path.open("w") as f:
        json.dump(content, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    print("Q-Verse 4x4 Final Bootstrap V11 Started")
    results = []
    for script in BOOTSTRAPS:
        result = run_script(script, force=args.force)
        results.append(result)
    generate_final_report(results)
    print("[SUMMARY]")
    print("[RUNTIME] Background Runtime")
    print("[MEMORY] Unified Memory")
    print("[CLIENTS] IDE/Web/GitHub")
    print("[AI] Multi Provider Runtime")
    print("[REPORT] reports/qverse_4x4_final_v11.json")
    print("Q-Verse 4x4 Final Bootstrap V11 Complete")

if __name__ == '__main__':
    main()
