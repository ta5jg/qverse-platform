from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NodejsInstallerService:
    name: str = "nodejs"
    enabled: bool = True

    def install_plan(self) -> dict:
        return {
            "service": self.name,
            "enabled": self.enabled,
            "steps": [
                "validate",
                "install",
                "configure",
                "start",
                "health_check",
            ],
        }

    def health(self) -> dict:
        return {
            "service": self.name,
            "healthy": True,
            "status": "ready",
        }


service = NodejsInstallerService()
