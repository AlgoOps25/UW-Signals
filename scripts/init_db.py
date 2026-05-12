"""Initialize the local UW-Signals database.

Usage:
    python scripts/init_db.py
"""

from __future__ import annotations

from src.storage import initialize_database


if __name__ == "__main__":
    initialize_database()
    print("UW-Signals database initialized.")
