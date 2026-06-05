

from typing import Any, Dict

from api.services.database_service import database_service


class DatabaseDependency:
    """Database dependency helper."""

    def connection_info(self) -> Dict[str, Any]:
        return database_service.get_connection_info()

    def health(self) -> Dict[str, Any]:
        return database_service.health_check()

    def execute(self, query: str) -> Dict[str, Any]:
        return database_service.execute_query(query)

    def tables(self) -> list[str]:
        return database_service.list_tables()

    def metrics(self) -> Dict[str, Any]:
        return database_service.get_metrics()


database_dependency = DatabaseDependency()