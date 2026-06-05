from __future__ import annotations

from typing import Any, Dict

CONFIG_VERSION = "V9"
DEFAULT_ENVIRONMENT = "development"


def get_config() -> Dict[str, Any]:
    return {
        "version": CONFIG_VERSION,
        "environment": DEFAULT_ENVIRONMENT,
        "installer": "qverse-platform",
    }


def validate_config(config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    current = config or get_config()
    return {
        "valid": bool(current.get("version")),
        "version": current.get("version"),
        "environment": current.get("environment"),
    }
