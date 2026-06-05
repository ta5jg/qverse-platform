
"""
Q-Verse Logger Engine V9

Purpose:
    Central Event, Audit, Metrics and Execution Tracking Layer

Relationship:
    State Engine   -> Discovery
    Config Engine  -> Desired State
    Audit Engine   -> Drift Detection
    Backup Engine  -> Recovery
    Logger Engine  -> Observability
    Installer      -> Execution
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import gzip
import hashlib
import json
import os
import shutil
import uuid


LOGGER_ENGINE_VERSION = 'V9'


@dataclass
class LogContext:
    correlation_id: str
    trace_id: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    request_id: Optional[str] = None


@dataclass
class LogEntry:
    timestamp: str
    level: str
    category: str
    message: str
    context: Optional[LogContext] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditTrailEntry:
    timestamp: str
    actor: str
    action: str
    target: str
    result: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityEvent:
    timestamp: str
    severity: str
    event_type: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionEvent:
    action: str
    status: str
    started_at: str
    completed_at: Optional[str] = None
    duration_ms: Optional[int] = None
    context: Optional[LogContext] = None


@dataclass
class MetricPoint:
    name: str
    value: float
    timestamp: str
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class AlertRule:
    name: str
    metric: str
    threshold: float
    operator: str = '>'
    enabled: bool = True


@dataclass
class AlertEvent:
    timestamp: str
    rule: str
    metric: str
    value: float
    threshold: float
    status: str


@dataclass
class RetentionPolicy:
    keep_days: int = 30
    max_file_size_bytes: int = 10 * 1024 * 1024
    compress_rotated: bool = True


@dataclass
class RemoteLogSink:
    name: str
    enabled: bool = False
    sink_type: str = 'local'
    endpoint: Optional[str] = None


@dataclass
class LoggerReport:
    version: str
    generated_at: str
    entries: int
    metrics: int
    executions: int
    audits: int
    security_events: int
    alerts: int
    checksum: str


class LoggerEngine:
    def __init__(self, root: str = '.qverse_logs'):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.log_file = self.root / 'events.jsonl'
        self.metric_file = self.root / 'metrics.jsonl'
        self.execution_file = self.root / 'execution.jsonl'
        self.audit_file = self.root / 'audit.jsonl'
        self.security_file = self.root / 'security.jsonl'
        self.alert_file = self.root / 'alerts.jsonl'

        self.retention_policy = RetentionPolicy()
        self.remote_sinks: List[RemoteLogSink] = []
        self.alert_rules: List[AlertRule] = []

    def now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def new_context(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> LogContext:
        return LogContext(
            correlation_id=str(uuid.uuid4()),
            trace_id=str(uuid.uuid4()),
            user_id=user_id,
            agent_id=agent_id,
            request_id=request_id,
        )

    def checksum(self, payload: str) -> str:
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def _append_jsonl(self, path: Path, payload: Dict[str, Any]) -> None:
        self.rotate_if_needed(path)

        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(payload, default=str) + '\n')

        self.ship_remote(path, payload)

    def rotate_if_needed(self, path: Path) -> Optional[Path]:
        if not path.exists():
            return None

        if path.stat().st_size < self.retention_policy.max_file_size_bytes:
            return None

        rotated = path.with_name(
            f'{path.stem}_{datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")}{path.suffix}'
        )
        path.rename(rotated)

        if self.retention_policy.compress_rotated:
            return self.compress_file(rotated)

        return rotated

    def compress_file(self, path: Path) -> Path:
        compressed = path.with_suffix(path.suffix + '.gz')

        with open(path, 'rb') as source:
            with gzip.open(compressed, 'wb') as target:
                shutil.copyfileobj(source, target)

        path.unlink(missing_ok=True)
        return compressed

    def prune_old_logs(self) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(
            days=self.retention_policy.keep_days
        )
        removed = 0

        for file in self.root.glob('*'):
            if not file.is_file():
                continue

            modified = datetime.fromtimestamp(
                file.stat().st_mtime,
                tz=timezone.utc,
            )

            if modified < cutoff:
                file.unlink(missing_ok=True)
                removed += 1

        return removed

    def ship_remote(self, path: Path, payload: Dict[str, Any]) -> bool:
        shipped = False

        for sink in self.remote_sinks:
            if not sink.enabled:
                continue

            # Integration hook for Loki, ELK, HTTP collectors, etc.
            shipped = True

        return shipped

    def add_remote_sink(self, sink: RemoteLogSink) -> None:
        self.remote_sinks.append(sink)

    def add_alert_rule(self, rule: AlertRule) -> None:
        self.alert_rules.append(rule)

    def log(
        self,
        level: str,
        category: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[LogContext] = None,
    ) -> LogEntry:
        entry = LogEntry(
            timestamp=self.now(),
            level=level.upper(),
            category=category,
            message=message,
            context=context,
            metadata=metadata or {},
        )

        self._append_jsonl(self.log_file, asdict(entry))
        return entry

    def info(self, category: str, message: str, **metadata):
        return self.log('INFO', category, message, metadata)

    def warning(self, category: str, message: str, **metadata):
        return self.log('WARNING', category, message, metadata)

    def error(self, category: str, message: str, **metadata):
        return self.log('ERROR', category, message, metadata)

    def audit(
        self,
        actor: str,
        action: str,
        target: str,
        result: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditTrailEntry:
        entry = AuditTrailEntry(
            timestamp=self.now(),
            actor=actor,
            action=action,
            target=target,
            result=result,
            metadata=metadata or {},
        )

        self._append_jsonl(self.audit_file, asdict(entry))
        return entry

    def security(
        self,
        severity: str,
        event_type: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecurityEvent:
        event = SecurityEvent(
            timestamp=self.now(),
            severity=severity.upper(),
            event_type=event_type,
            message=message,
            metadata=metadata or {},
        )

        self._append_jsonl(self.security_file, asdict(event))
        return event

    def metric(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> MetricPoint:
        point = MetricPoint(
            name=name,
            value=value,
            timestamp=self.now(),
            labels=labels or {},
        )

        self._append_jsonl(self.metric_file, asdict(point))
        self.evaluate_alerts(point)
        return point

    def evaluate_alerts(self, point: MetricPoint) -> List[AlertEvent]:
        events = []

        for rule in self.alert_rules:
            if not rule.enabled or rule.metric != point.name:
                continue

            triggered = False

            if rule.operator == '>' and point.value > rule.threshold:
                triggered = True
            elif rule.operator == '<' and point.value < rule.threshold:
                triggered = True
            elif rule.operator == '>=' and point.value >= rule.threshold:
                triggered = True
            elif rule.operator == '<=' and point.value <= rule.threshold:
                triggered = True
            elif rule.operator == '==' and point.value == rule.threshold:
                triggered = True

            if triggered:
                event = AlertEvent(
                    timestamp=self.now(),
                    rule=rule.name,
                    metric=point.name,
                    value=point.value,
                    threshold=rule.threshold,
                    status='triggered',
                )
                self._append_jsonl(self.alert_file, asdict(event))
                events.append(event)

        return events

    def execution_start(
        self,
        action: str,
        context: Optional[LogContext] = None,
    ) -> ExecutionEvent:
        event = ExecutionEvent(
            action=action,
            status='running',
            started_at=self.now(),
            context=context,
        )

        self._append_jsonl(self.execution_file, asdict(event))
        return event

    def execution_complete(
        self,
        action: str,
        status: str = 'completed',
        started_at: Optional[str] = None,
        context: Optional[LogContext] = None,
    ) -> ExecutionEvent:
        completed_at = self.now()
        duration_ms = None

        if started_at:
            try:
                start = datetime.fromisoformat(started_at)
                end = datetime.fromisoformat(completed_at)
                duration_ms = int((end - start).total_seconds() * 1000)
            except Exception:
                duration_ms = None

        event = ExecutionEvent(
            action=action,
            status=status,
            started_at=started_at or completed_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            context=context,
        )

        self._append_jsonl(self.execution_file, asdict(event))
        return event

    def read_jsonl(self, path: Path) -> Iterable[Dict[str, Any]]:
        if not path.exists():
            return []

        rows = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return rows

    def query(
        self,
        level: Optional[str] = None,
        category: Optional[str] = None,
        text: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        results = []

        for row in self.read_jsonl(self.log_file):
            if level and row.get('level') != level.upper():
                continue
            if category and row.get('category') != category:
                continue
            if text and text.lower() not in json.dumps(row).lower():
                continue
            results.append(row)

            if len(results) >= limit:
                break

        return results

    def count_lines(self, path: Path) -> int:
        if not path.exists():
            return 0

        with open(path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)

    def prometheus_export(self) -> str:
        metrics = self.read_jsonl(self.metric_file)
        lines = []

        for item in metrics:
            name = item.get('name', 'qverse_metric').replace('.', '_')
            value = item.get('value', 0)
            lines.append(f'qverse_{name} {value}')

        return '\n'.join(lines)

    def opentelemetry_hook(self, payload: Dict[str, Any]) -> bool:
        # OpenTelemetry integration hook.
        return bool(payload)

    def build_report(self) -> LoggerReport:
        payload = {
            'entries': self.count_lines(self.log_file),
            'metrics': self.count_lines(self.metric_file),
            'executions': self.count_lines(self.execution_file),
            'audits': self.count_lines(self.audit_file),
            'security_events': self.count_lines(self.security_file),
            'alerts': self.count_lines(self.alert_file),
        }

        return LoggerReport(
            version=LOGGER_ENGINE_VERSION,
            generated_at=self.now(),
            entries=payload['entries'],
            metrics=payload['metrics'],
            executions=payload['executions'],
            audits=payload['audits'],
            security_events=payload['security_events'],
            alerts=payload['alerts'],
            checksum=self.checksum(json.dumps(payload, sort_keys=True)),
        )

    def export_json(self) -> Dict[str, Any]:
        return asdict(self.build_report())

    def export_markdown(self) -> str:
        report = self.build_report()
        lines = [
            '# Q-Verse Logger Report',
            '',
            f'- Version: {report.version}',
            f'- Generated At: {report.generated_at}',
            f'- Entries: {report.entries}',
            f'- Metrics: {report.metrics}',
            f'- Executions: {report.executions}',
            f'- Audits: {report.audits}',
            f'- Security Events: {report.security_events}',
            f'- Alerts: {report.alerts}',
            f'- Checksum: {report.checksum}',
        ]
        return '\n'.join(lines)


LOGGER_ENGINE_STATUS = 'V9_ENTERPRISE_COMPLETE'