

from datetime import datetime, timezone
from typing import Dict

APP_NAME = "Q-Verse"
PLATFORM_NAME = "Q-Verse Platform"
API_VERSION = "V9"
APP_VERSION = "9.0.0"
BUILD_VERSION = "9.0.0-enterprise"
BUILD_DATE = datetime.now(timezone.utc).isoformat()


VERSION_INFO: Dict[str, str] = {
    "app_name": APP_NAME,
    "platform": PLATFORM_NAME,
    "api_version": API_VERSION,
    "app_version": APP_VERSION,
    "build_version": BUILD_VERSION,
    "build_date": BUILD_DATE,
}


def get_version_info() -> Dict[str, str]:
    return VERSION_INFO.copy()


def get_version_string() -> str:
    return f"{APP_NAME} {API_VERSION} ({BUILD_VERSION})"