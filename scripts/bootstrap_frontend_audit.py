#!/usr/bin/env python3
"""Q-Verse V9 Frontend Audit Engine.

Audits React/Vite frontend structure and reports health.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend" / "src"

PLACEHOLDER_PATTERNS = [
    "Q-Verse Card Component",
    "Q-Verse Header Component",
    "TODO:",
    "FIXME:",
    "placeholder_component",
]


def collect(pattern: str):
    if not FRONTEND.exists():
        return []
    return sorted(FRONTEND.rglob(pattern))


components = collect("*.jsx")
pages = [p for p in collect("*.jsx") if "pages" in str(p)]
hooks = collect("*.js")

empty_files = []
placeholder_files = []

for file in FRONTEND.rglob("*"):
    if not file.is_file():
        continue

    try:
        content = file.read_text(encoding="utf-8")
    except Exception:
        continue

    if len(content.strip()) == 0:
        empty_files.append(str(file.relative_to(ROOT)))
        continue

    if len(content.strip()) > 100:
        continue

    if any(token in content for token in PLACEHOLDER_PATTERNS):
        placeholder_files.append(str(file.relative_to(ROOT)))


route_file = FRONTEND / "routes" / "index.jsx"
route_status = "missing"

if route_file.exists():
    route_status = "present"


health_score = 100
health_score -= len(empty_files) * 10
health_score -= len(placeholder_files) * 2
health_score = max(0, health_score)

repair_targets = sorted(set(empty_files + placeholder_files))

report = {
    "frontend_version": "V9",
    "components": len(components),
    "pages": len(pages),
    "hooks_and_js": len(hooks),
    "empty_files": empty_files,
    "placeholder_files": placeholder_files,
    "repair_targets": repair_targets,
    "total_repairs_needed": len(repair_targets),
    "route_registry": route_status,
    "frontend_health": health_score,
    "frontend_status": (
        "healthy"
        if not repair_targets
        else "needs_repair"
    ),
}

print(json.dumps(report, indent=2))