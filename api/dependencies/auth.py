from typing import Dict, Optional

from api.core.security import security_context, token_manager


class AuthDependency:
    """Authentication dependency helper."""

    def authenticate(self, username: str) -> Dict[str, str]:
        security_context.current_user = username
        return token_manager.create_token(username)

    def current_user(self) -> Optional[str]:
        return security_context.current_user

    def is_authenticated(self) -> bool:
        return security_context.current_user is not None

    def logout(self) -> None:
        security_context.current_user = None


auth_dependency = AuthDependency()
