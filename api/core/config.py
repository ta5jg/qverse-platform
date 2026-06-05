

from pathlib import Path
from typing import Any, Dict, Optional

from api.core.settings import settings


class ConfigRegistry:
    def __init__(self) -> None:
        self._configs: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._configs[key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._configs.get(key, default)

    def has(self, key: str) -> bool:
        return key in self._configs

    def remove(self, key: str) -> None:
        self._configs.pop(key, None)

    def all(self) -> Dict[str, Any]:
        return self._configs.copy()


class ConfigLoader:
    def __init__(self, registry: ConfigRegistry) -> None:
        self.registry = registry

    def load_defaults(self) -> None:
        self.registry.set("app_name", settings.app_name)
        self.registry.set("platform_name", settings.platform_name)
        self.registry.set("environment", settings.environment)
        self.registry.set("api_version", settings.api_version)
        self.registry.set("database_url", settings.database_url)

    def load_from_dict(self, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            self.registry.set(key, value)

    def load_from_env_file(self, env_path: str) -> Path:
        path = Path(env_path)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {env_path}")

        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            self.registry.set(key.strip(), value.strip())

        return path


config_registry = ConfigRegistry()
config_loader = ConfigLoader(config_registry)
config_loader.load_defaults()