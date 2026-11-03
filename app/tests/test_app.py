import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "Azure Production API"
    assert data["status"] == "running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_transaction_missing_description(client):
    response = client.post(
        "/transactions",
        json={"amount": "125.50"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Valid description required"


def test_transaction_invalid_amount(client):
    response = client.post(
        "/transactions",
        json={
            "description": "Invalid transaction",
            "amount": "not-a-number"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Valid amount required"
