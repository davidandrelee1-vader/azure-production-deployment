from pathlib import Path
import os
import psycopg

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def run_migrations():
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    if not files:
        raise RuntimeError("No migration files found")

    with psycopg.connect(connect_timeout=5) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR(255) PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)

        conn.commit()

        for file in files:
            version = file.name

            with conn.transaction():
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM schema_migrations WHERE version = %s",
                        (version,)
                    )

                    if cursor.fetchone():
                        print(f"SKIPPED: {version}")
                        continue

                    print(f"APPLYING: {version}")

                    sql = file.read_text(encoding="utf-8")
                    cursor.execute(sql)

                    cursor.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s)",
                        (version,)
                    )

                    print(f"APPLIED: {version}")


if __name__ == "__main__":
    run_migrations()
