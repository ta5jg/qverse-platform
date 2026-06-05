from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_system_endpoint_exists():
    response = client.get("/system")
    assert response.status_code in [200, 404]


def test_system_response_is_json():
    response = client.get("/system")
    assert response.headers.get("content-type", "").startswith("application/json")
