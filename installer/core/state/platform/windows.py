from __future__ import annotations

from installer.core.state.platform.base import PlatformAdapter


class WindowsPlatformAdapter(PlatformAdapter):
    def __init__(self) -> None:
        super().__init__(name="windows")

    def requirements(self) -> list[str]:
        return ["python", "node", "npm"]
