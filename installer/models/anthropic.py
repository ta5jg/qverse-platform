from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnthropicProvider:
    name: str = "anthropic"
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


provider = AnthropicProvider()
