from __future__ import annotations

from typing import Any, Dict, Optional


class QVerseException(Exception):
    """Base exception for the Q-Verse platform."""

    def __init__(
        self,
        message: str,
        error_code: str = "QVERSE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class ValidationException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "VALIDATION_ERROR", details)


class AuthenticationException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "AUTHENTICATION_ERROR", details)


class AuthorizationException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "AUTHORIZATION_ERROR", details)


class ResourceNotFoundException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "RESOURCE_NOT_FOUND", details)


class ConflictException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "CONFLICT", details)


class ConfigurationException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "CONFIGURATION_ERROR", details)


class DatabaseException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "DATABASE_ERROR", details)


class IntegrationException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "INTEGRATION_ERROR", details)


class ServiceException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "SERVICE_ERROR", details)


class EngineException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "ENGINE_ERROR", details)


class DeploymentException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "DEPLOYMENT_ERROR", details)


class WorkflowException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "WORKFLOW_ERROR", details)


class TaskException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "TASK_ERROR", details)


class AuditException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "AUDIT_ERROR", details)


class TelemetryException(QVerseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, "TELEMETRY_ERROR", details)


def exception_to_dict(exc: QVerseException) -> Dict[str, Any]:
    return {
        "error": exc.error_code,
        "message": exc.message,
        "details": exc.details,
    }
