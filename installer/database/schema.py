DATABASE_SCHEMA = {
    "version": "V9",
    "tables": [
        "projects",
        "agents",
        "workflows",
        "tasks",
        "models",
        "audit_events",
        "telemetry_events",
    ],
}


def get_schema() -> dict:
    return DATABASE_SCHEMA.copy()
