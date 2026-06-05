

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from api.core.logging import logger
from api.services.telemetry_service import telemetry_service


class TelemetryEngine:
    """Telemetry collection and analytics engine."""

    def record_metric(
        self,
        metric_name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        metric = telemetry_service.record_metric(
            metric_name=metric_name,
            value=value,
            labels=labels,
        )

        logger.info(
            f"Telemetry metric recorded: {metric_name}",
            source="telemetry_engine",
        )

        return metric

    def record_event(
        self,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return telemetry_service.record_event(
            event_type=event_type,
            payload=payload,
        )

    def list_metrics(self) -> List[Dict[str, Any]]:
        return telemetry_service.list_metrics()

    def list_events(self) -> List[Dict[str, Any]]:
        return telemetry_service.list_events()

    def clear_metrics(self) -> None:
        telemetry_service.clear_metrics()

    def clear_events(self) -> None:
        telemetry_service.clear_events()

    def health(self) -> Dict[str, Any]:
        return {
            "healthy": True,
            "engine": "telemetry_engine",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "health": self.health(),
            "metrics": self.get_metrics(),
            "metric_count": len(self.list_metrics()),
            "event_count": len(self.list_events()),
        }

    def get_metrics(self) -> Dict[str, Any]:
        summary = telemetry_service.get_metrics_summary()

        return {
            "engine": "telemetry_engine",
            **summary,
        }


telemetry_engine = TelemetryEngine()