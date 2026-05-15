"""Database storage helpers for UW-Signals."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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
    """Create MVP tables."""
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
                CREATE TABLE IF NOT EXISTS raw_discord_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discord_message_id TEXT NOT NULL UNIQUE,
                    channel_id TEXT NOT NULL,
                    channel_name TEXT,
                    author_id TEXT,
                    author_name TEXT,
                    created_at TEXT,
                    received_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    content TEXT,
                    embeds_json TEXT,
                    parsed_json TEXT,
                    raw_json TEXT NOT NULL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS discord_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    summary_timestamp TEXT NOT NULL,
                    window_seconds INTEGER NOT NULL,
                    summary_text TEXT NOT NULL,
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


def utc_now_iso() -> str:
    """Return current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat()


def insert_raw_discord_message(
    engine: Engine,
    *,
    discord_message_id: str,
    channel_id: str,
    channel_name: str | None,
    author_id: str | None,
    author_name: str | None,
    created_at: str | None,
    content: str | None,
    embeds: list[dict[str, Any]],
    parsed: dict[str, Any],
    raw: dict[str, Any],
) -> bool:
    """Insert a Discord message, returning False if it already exists."""
    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                INSERT OR IGNORE INTO raw_discord_messages (
                    discord_message_id,
                    channel_id,
                    channel_name,
                    author_id,
                    author_name,
                    created_at,
                    content,
                    embeds_json,
                    parsed_json,
                    raw_json
                ) VALUES (
                    :discord_message_id,
                    :channel_id,
                    :channel_name,
                    :author_id,
                    :author_name,
                    :created_at,
                    :content,
                    :embeds_json,
                    :parsed_json,
                    :raw_json
                )
                """
            ),
            {
                "discord_message_id": discord_message_id,
                "channel_id": channel_id,
                "channel_name": channel_name,
                "author_id": author_id,
                "author_name": author_name,
                "created_at": created_at,
                "content": content,
                "embeds_json": json.dumps(embeds, default=str),
                "parsed_json": json.dumps(parsed, default=str),
                "raw_json": json.dumps(raw, default=str),
            },
        )
        return result.rowcount > 0


def fetch_recent_discord_messages(engine: Engine, window_seconds: int) -> list[dict[str, Any]]:
    """Fetch parsed Discord messages received in the last window."""
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                """
                SELECT *
                FROM raw_discord_messages
                WHERE received_at >= datetime('now', :window_modifier)
                ORDER BY received_at DESC
                """
            ),
            {"window_modifier": f"-{window_seconds} seconds"},
        ).mappings()
        return [dict(row) for row in rows]


def insert_discord_summary(
    engine: Engine,
    *,
    window_seconds: int,
    summary_text: str,
    payload: dict[str, Any],
) -> None:
    """Store a generated Discord summary."""
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO discord_summaries (
                    summary_timestamp,
                    window_seconds,
                    summary_text,
                    payload_json
                ) VALUES (
                    :summary_timestamp,
                    :window_seconds,
                    :summary_text,
                    :payload_json
                )
                """
            ),
            {
                "summary_timestamp": utc_now_iso(),
                "window_seconds": window_seconds,
                "summary_text": summary_text,
                "payload_json": json.dumps(payload, default=str),
            },
        )
