from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SignalIntegration:
    name: str = "signal"
    enabled: bool = True

    def config_schema(self) -> dict:
        return {
            "integration": self.name,
            "enabled": self.enabled,
            "required_keys": [],
        }

    def health(self) -> dict:
        return {
            "integration": self.name,
            "healthy": True,
            "status": "ready",
        }


integration = SignalIntegration()
