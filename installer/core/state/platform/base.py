from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PlatformAdapter:
    name: str = "generic"

    def detect(self) -> Dict[str, str]:
        return {
            "platform": self.name,
            "status": "detected",
        }

    def validate(self) -> Dict[str, bool]:
        return {
            "supported": True,
            "ready": True,
        }

    def requirements(self) -> list[str]:
        return []
