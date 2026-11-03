import os
import uuid
from decimal import Decimal

import psycopg
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def test_database():
    # Refuse to run unless explicitly using testdb.
    if os.getenv("PGDATABASE") != "testdb":
        pytest.fail(
            "Safety check failed: PGDATABASE must be testdb."
        )

    # Your Flask routes use psycopg.connect() with PG* settings.
    with psycopg.connect(connect_timeout=5) as conn:
        if conn.info.dbname != "testdb":
            pytest.fail("Connected to an unexpected database.")

        yield conn


def test_database_health(client, test_database):
    response = client.get("/db-health")

    assert response.status_code == 200
    assert response.get_json()["database"] == "connected"


def test_create_and_retrieve_transaction(client, test_database):
    description = f"integration-test-{uuid.uuid4().hex}"
    transaction_id = None

    try:
        response = client.post(
            "/transactions",
            json={
                "description": description,
                "amount": "125.50"
            }
        )

        assert response.status_code == 201

        created = response.get_json()
        transaction_id = created["id"]

        assert created["description"] == description
        assert Decimal(created["amount"]) == Decimal("125.50")

        response = client.get("/transactions")
        assert response.status_code == 200

        transactions = response.get_json()
        matching = [
            item for item in transactions
            if item["id"] == transaction_id
        ]

        assert len(matching) == 1
        assert matching[0]["description"] == description
        assert Decimal(matching[0]["amount"]) == Decimal("125.50")

    finally:
        if transaction_id is not None:
            with test_database.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM transactions WHERE id = %s",
                    (transaction_id,)
                )
            test_database.commit()
