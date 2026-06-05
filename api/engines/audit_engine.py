

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from api.core.logging import logger
from api.services.audit_service import audit_service


class AuditEngine:
    """Audit execution and reporting engine."""

    def create_report(
        self,
        report_id: str,
        target: str,
        findings: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        report = audit_service.create_report(
            report_id=report_id,
            target=target,
            findings=findings,
        )

        logger.info(
            f"Audit engine created report: {report_id}",
            source="audit_engine",
        )

        return report

    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        return audit_service.get_report(report_id)

    def list_reports(self) -> List[Dict[str, Any]]:
        return audit_service.list_reports()

    def record_event(
        self,
        action: str,
        actor: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return audit_service.record_event(action, actor, details)

    def list_events(self) -> List[Dict[str, Any]]:
        return audit_service.list_events()

    def health(self) -> Dict[str, Any]:
        return {
            "healthy": True,
            "engine": "audit_engine",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "health": self.health(),
            "metrics": self.get_metrics(),
            "reports": len(self.list_reports()),
            "events": len(self.list_events()),
        }

    def get_metrics(self) -> Dict[str, Any]:
        metrics = audit_service.get_metrics()

        return {
            "engine": "audit_engine",
            **metrics,
        }


audit_engine = AuditEngine()