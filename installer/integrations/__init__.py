"""Q-Verse Installer Integrations V9."""

INSTALLER_INTEGRATIONS = [
    "discord",
    "email",
    "signal",
    "slack",
    "telegram",
    "whatsapp",
]


def list_installer_integrations() -> list[str]:
    return INSTALLER_INTEGRATIONS.copy()
