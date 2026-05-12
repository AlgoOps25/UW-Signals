"""Post-alert outcome tracking helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OutcomeSnapshot:
    alert_id: int
    check_timestamp: datetime
    window_minutes: int
    underlying_price: float | None = None
    option_price: float | None = None
    max_favorable_excursion: float | None = None
    max_adverse_excursion: float | None = None
    notes: str = ""


def classify_outcome(
    max_favorable_excursion: float | None,
    max_adverse_excursion: float | None,
    target: float,
    invalidation: float,
) -> str:
    """Classify whether an alert was useful after a tracking window.

    This is intentionally generic. For options, MFE/MAE may be premium movement.
    For underlying, it may be points or percent movement.
    """
    mfe = max_favorable_excursion or 0.0
    mae = abs(max_adverse_excursion or 0.0)

    if mfe >= target and mae < invalidation:
        return "target_before_invalidation"
    if mae >= invalidation and mfe < target:
        return "invalidation_before_target"
    if mfe > mae:
        return "favorable_but_unresolved"
    if mae > mfe:
        return "adverse_but_unresolved"
    return "flat_or_unknown"
