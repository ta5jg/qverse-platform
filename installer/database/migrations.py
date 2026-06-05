from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MigrationPlan:
    version: str = "V9"
    migrations: list[str] = field(default_factory=list)

    def add(self, migration: str) -> None:
        self.migrations.append(migration)

    def plan(self) -> dict:
        return {
            "version": self.version,
            "migrations": self.migrations,
            "total": len(self.migrations),
        }
