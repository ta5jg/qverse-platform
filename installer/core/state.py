from __future__ import annotations

from typing import Any, Dict

from installer.core.state.discovery import DiscoveryState
from installer.core.state.compliance import ComplianceState
from installer.core.state.snapshot import SnapshotState


class StateEngine:
    def overview(self) -> Dict[str, Any]:
        return {
            "discovery": DiscoveryState().status(),
            "compliance": ComplianceState().status(),
            "snapshot": SnapshotState().status(),
        }

    def health(self) -> Dict[str, Any]:
        return {
            "healthy": True,
            "engine": "state",
            "modules": self.overview(),
        }


state_engine = StateEngine()
