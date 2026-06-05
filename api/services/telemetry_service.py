from __future__ import annotations

from datetime import datetime, timezone


class TelemetryService:
    def health(self):
        return {
            "healthy": True,
            "service": "telemetry_service",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def metrics(self):
        return {
            "service": "telemetry_service",
            "healthy": True,
        }


telemetry_service = TelemetryService()
