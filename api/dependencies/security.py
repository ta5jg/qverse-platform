

from typing import Optional

from api.core.security import (
    permission_manager,
    security_context,
)


class SecurityDependency:
    """Authorization and permission dependency helper."""

    def current_user(self) -> Optional[str]:
        return security_context.current_user

    def has_permission(self, permission: str) -> bool:
        user = security_context.current_user

        if not user:
            return False

        return permission_manager.has_permission(user, permission)

    def require_permission(self, permission: str) -> bool:
        return self.has_permission(permission)

    def grant(self, permission: str) -> bool:
        user = security_context.current_user

        if not user:
            return False

        permission_manager.grant(user, permission)
        return True

    def revoke(self, permission: str) -> bool:
        user = security_context.current_user

        if not user:
            return False

        permission_manager.revoke(user, permission)
        return True


security_dependency = SecurityDependency()