from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


class SnapshotState:
    def status(self) -> Dict[str, Any]:
        return {
            "module": "snapshot",
            "healthy": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
