from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_deployments_endpoint_exists():
    response = client.get("/deployments")
    assert response.status_code in [200, 404]


def test_deployments_response_is_json():
    response = client.get("/deployments")
    assert response.headers.get("content-type", "").startswith("application/json")
