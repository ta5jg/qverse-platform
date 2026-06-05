from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SeedPlan:
    version: str = "V9"
    records: list[dict[str, Any]] = field(default_factory=list)

    def add(self, table: str, data: dict[str, Any]) -> None:
        self.records.append({"table": table, "data": data})

    def plan(self) -> dict:
        return {
            "version": self.version,
            "records": self.records,
            "total": len(self.records),
        }
