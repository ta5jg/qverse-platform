"""Q-Verse Installer Services V9."""

INSTALLER_SERVICES = [
    "certbot",
    "docker",
    "nginx",
    "nodejs",
    "postgres",
    "qverse_api",
    "redis",
    "n8n",
]


def list_installer_services() -> list[str]:
    return INSTALLER_SERVICES.copy()
