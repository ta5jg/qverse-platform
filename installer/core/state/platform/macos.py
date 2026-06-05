from __future__ import annotations

from installer.core.state.platform.base import PlatformAdapter


class MacOSPlatformAdapter(PlatformAdapter):
    def __init__(self) -> None:
        super().__init__(name="macos")

    def requirements(self) -> list[str]:
        return ["python3", "node", "npm"]
