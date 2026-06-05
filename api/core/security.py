

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional


class SecurityContext:
    def __init__(self) -> None:
        self.current_user: Optional[str] = None
        self.roles: List[str] = []
        self.permissions: List[str] = []


class PermissionManager:
    def __init__(self) -> None:
        self._permissions: Dict[str, List[str]] = {}

    def grant(self, subject: str, permission: str) -> None:
        self._permissions.setdefault(subject, []).append(permission)

    def revoke(self, subject: str, permission: str) -> None:
        if subject in self._permissions:
            self._permissions[subject] = [p for p in self._permissions[subject] if p != permission]

    def has_permission(self, subject: str, permission: str) -> bool:
        return permission in self._permissions.get(subject, [])


class TokenManager:
    def create_token(self, subject: str, expires_minutes: int = 60) -> Dict[str, str]:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        return {
            "subject": subject,
            "expires_at": expires_at.isoformat(),
        }


class SecurityAudit:
    def __init__(self) -> None:
        self.events: List[Dict[str, str]] = []

    def record(self, action: str, actor: str) -> None:
        self.events.append(
            {
                "action": action,
                "actor": actor,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )


security_context = SecurityContext()
permission_manager = PermissionManager()
token_manager = TokenManager()
security_audit = SecurityAudit()