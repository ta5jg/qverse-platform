

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class LogRecord:
    def __init__(
        self,
        level: str,
        message: str,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.timestamp = datetime.now(timezone.utc)
        self.level = level.upper()
        self.message = message
        self.source = source
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "source": self.source,
            "metadata": self.metadata,
        }


class Logger:
    def __init__(self) -> None:
        self.records: List[LogRecord] = []

    def log(
        self,
        level: str,
        message: str,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> LogRecord:
        record = LogRecord(level, message, source, metadata)
        self.records.append(record)
        return record

    def info(self, message: str, source: Optional[str] = None) -> LogRecord:
        return self.log("INFO", message, source)

    def warning(self, message: str, source: Optional[str] = None) -> LogRecord:
        return self.log("WARNING", message, source)

    def error(self, message: str, source: Optional[str] = None) -> LogRecord:
        return self.log("ERROR", message, source)

    def critical(self, message: str, source: Optional[str] = None) -> LogRecord:
        return self.log("CRITICAL", message, source)

    def all(self) -> List[Dict[str, Any]]:
        return [record.to_dict() for record in self.records]

    def clear(self) -> None:
        self.records.clear()


class LogMetrics:
    def __init__(self) -> None:
        self.total_logs = 0

    def record(self) -> None:
        self.total_logs += 1


logger = Logger()
log_metrics = LogMetrics()