from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LmstudioProvider:
    name: str = "lmstudio"
    enabled: bool = True

    def status(self) -> dict:
        return {
            "provider": self.name,
            "enabled": self.enabled,
            "status": "ready",
        }

    def validate(self) -> dict:
        return {
            "provider": self.name,
            "valid": True,
        }


provider = LmstudioProvider()
