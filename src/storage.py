"""Database storage helpers for UW-Signals."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.config import get_settings


def get_engine(database_url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine from settings or explicit URL."""
    settings = get_settings()
    url = database_url or settings.database_url

    if url.startswith("sqlite:///"):
        db_path = url.replace("sqlite:///", "", 1)
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    return create_engine(url, future=True)


def initialize_database(engine: Engine | None = None) -> None:
    """Create initial MVP tables.

    This schema is intentionally lightweight. It will be expanded after UW response
    shapes are confirmed.
    """
    engine = engine or get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS raw_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    ticker TEXT,
                    event_timestamp TEXT,
                    received_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    payload_json TEXT NOT NULL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS signal_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_timestamp TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    title TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    regime TEXT NOT NULL,
                    score REAL NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS alert_outcomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id INTEGER NOT NULL,
                    check_timestamp TEXT NOT NULL,
                    window_minutes INTEGER NOT NULL,
                    underlying_price REAL,
                    option_price REAL,
                    max_favorable_excursion REAL,
                    max_adverse_excursion REAL,
                    notes TEXT,
                    FOREIGN KEY(alert_id) REFERENCES signal_alerts(id)
                )
                """
            )
        )
