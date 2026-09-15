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
    assert "Utility Hub" in response.text
    assert "Calculator" in response.text
    assert "CIDR Calculator" in response.text
    assert "Unit Converter" in response.text
    assert "Quick Notes" in response.text

def test_calculator_addition():
    response = client.post(
        "/api/v1/calculator",
        json={
            "operation": "add",
            "a": 10,
            "b": 5,
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == 15


def test_calculator_division_by_zero():
    response = client.post(
        "/api/v1/calculator",
        json={
            "operation": "divide",
            "a": 10,
            "b": 0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero."


def test_cidr_calculation():
    response = client.post(
        "/api/v1/cidr",
        params={"cidr": "192.168.1.0/24"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["network"] == "192.168.1.0"
    assert data["broadcast"] == "192.168.1.255"
    assert data["usable_hosts"] == 254


def test_unit_conversion():
    response = client.post(
        "/api/v1/convert",
        params={
            "category": "length",
            "from_unit": "km",
            "to_unit": "m",
            "value": 2.5,
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == 2500
