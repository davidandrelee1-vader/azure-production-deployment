
from flask import Flask, jsonify, request
from decimal import Decimal, InvalidOperation
import os
import psycopg

app = Flask(__name__)


# 1. Application information
@app.route("/")
def home():
    return jsonify({
        "application": "Azure Production API",
        "status": "running",
        "environment": os.getenv("APP_ENV", "development")
    })


# 2. Application health check
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


# 3. PostgreSQL connectivity check
@app.route("/db-health")
def db_health():
    try:
        with psycopg.connect(connect_timeout=5) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except psycopg.Error:
        app.logger.exception("Database health check failed")
        return jsonify({
            "status": "unhealthy",
            "database": "connection failed"
        }), 503


# 4. Create a transaction
@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "JSON object required"
        }), 400

    description = data.get("description")
    amount = data.get("amount")

    # Validate description
    if not isinstance(description, str) or not description.strip():
        return jsonify({
            "error": "Valid description required"
        }), 400

    description = description.strip()

    if len(description) > 255:
        return jsonify({
            "error": "Description too long"
        }), 400

    # Validate amount
    if isinstance(amount, bool) or not isinstance(amount, (int, float, str)):
        return jsonify({
            "error": "Valid amount required"
        }), 400

    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        return jsonify({
            "error": "Valid amount required"
        }), 400

    if not value.is_finite():
        return jsonify({
            "error": "Amount must be finite"
        }), 400

    if value.as_tuple().exponent < -2:
        return jsonify({
            "error": "Amount must have at most 2 decimal places"
        }), 400

    if abs(value) >= Decimal("10000000000"):
        return jsonify({
            "error": "Amount exceeds allowed range"
        }), 400

    # Insert transaction into PostgreSQL
    try:
        with psycopg.connect(connect_timeout=5) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO transactions (description, amount)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (description, value)
                )

                transaction_id = cursor.fetchone()[0]

        return jsonify({
            "status": "created",
            "id": transaction_id,
            "description": description,
            "amount": str(value)
        }), 201

    except psycopg.Error:
        app.logger.exception("Failed to create transaction")
        return jsonify({
            "error": "Database operation failed"
        }), 503


# 5. Retrieve transactions
@app.route("/transactions", methods=["GET"])
def get_transactions():
    try:
        with psycopg.connect(connect_timeout=5) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, description, amount, created_at
                    FROM transactions
                    ORDER BY id DESC
                    LIMIT 100
                    """
                )

                rows = cursor.fetchall()

        transactions = [
            {
                "id": row[0],
                "description": row[1],
                "amount": str(row[2]),
                "created_at": row[3].isoformat()
            }
            for row in rows
        ]

        return jsonify(transactions), 200

    except psycopg.Error:
        app.logger.exception("Failed to retrieve transactions")
        return jsonify({
            "error": "Database operation failed"
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
