from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_version_endpoint_returns_success():
    response = client.get("/version")

    assert response.status_code == 200


def test_metadata_endpoint_returns_target_platform():
    response = client.get("/metadata")

    assert response.status_code == 200
    assert response.json()["target_platform"] == "AWS ECS Fargate"
