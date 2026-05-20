"""
datetime_utils.py – Gemeinsame Zeit-Helfer.
"""
from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Aktuelle UTC-Zeit im bisherigen naiven datetime-Format zurückgeben."""
    # SQLite/SQLModel speichern die bestehenden Werte ohne tzinfo; das bleibt bewusst kompatibel.
    return datetime.now(UTC).replace(tzinfo=None)
