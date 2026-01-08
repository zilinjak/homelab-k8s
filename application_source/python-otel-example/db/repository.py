"""Database repository for HTTP results."""

import sqlite3
from datetime import datetime, timezone

from opentelemetry import trace

from db.config import DB_PATH

# Get tracer for manual instrumentation
tracer = trace.get_tracer(__name__)


def init_db():
    """Initialize SQLite database with results table."""
    with tracer.start_as_current_span("init_db"):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS http_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                status_code INTEGER NOT NULL,
                response_size INTEGER,
                delay_seconds REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()


def save_result(endpoint: str, status_code: int, response_size: int, delay: float) -> int:
    """Save HTTP request result to database."""
    with tracer.start_as_current_span("save_result_to_db") as span:
        span.set_attribute("db.system", "sqlite")
        span.set_attribute("db.name", DB_PATH)
        span.set_attribute("db.operation", "INSERT")
        span.set_attribute("http.endpoint", endpoint)
        span.set_attribute("http.status_code", status_code)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO http_results (endpoint, status_code, response_size, delay_seconds, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (endpoint, status_code, response_size, delay, datetime.now(timezone.utc))
        )
        conn.commit()
        inserted_id = cursor.lastrowid
        span.set_attribute("db.result.id", inserted_id)
        conn.close()
        return inserted_id


def get_all_results() -> list[dict]:
    """Get all stored results from the database."""
    with tracer.start_as_current_span("get_all_results") as span:
        span.set_attribute("db.system", "sqlite")
        span.set_attribute("db.name", DB_PATH)
        span.set_attribute("db.operation", "SELECT")

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM http_results ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        results = [dict(row) for row in rows]
        span.set_attribute("db.result.count", len(results))

        return results

