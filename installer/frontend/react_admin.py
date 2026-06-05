from __future__ import annotations

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
