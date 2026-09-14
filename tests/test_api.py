from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "azure-secure-network-platform",
    }


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200
    assert "Azure Secure Network Platform" in response.text
    assert "secure Azure networking" in response.text
