from __future__ import annotations

from installer.core.state.platform.base import PlatformAdapter


class LinuxPlatformAdapter(PlatformAdapter):
    def __init__(self) -> None:
        super().__init__(name="linux")

    def requirements(self) -> list[str]:
        return ["python3", "nginx", "docker", "postgresql", "redis"]
