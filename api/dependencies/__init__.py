

"""Q-Verse Dependencies Layer V9"""

from api.dependencies.auth import auth_dependency, AuthDependency
from api.dependencies.security import security_dependency, SecurityDependency
from api.dependencies.database import database_dependency, DatabaseDependency

__version__ = "V9"

__all__ = [
    "AuthDependency",
    "SecurityDependency",
    "DatabaseDependency",
    "auth_dependency",
    "security_dependency",
    "database_dependency",
]