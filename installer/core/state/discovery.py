from __future__ import annotations

from typing import Any, Dict


class DiscoveryState:
    def status(self) -> Dict[str, Any]:
        return {
            "module": "discovery",
            "healthy": True,
            "resources": ["api", "installer", "services", "models"],
        }
