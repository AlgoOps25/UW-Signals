"""Underlying price-action confirmation helpers."""

from __future__ import annotations

from src.models import Direction


def classify_price_confirmation(
    current_price: float | None,
    vwap: float | None = None,
    prior_high: float | None = None,
    prior_low: float | None = None,
    direction: Direction = Direction.UNKNOWN,
) -> tuple[float, list[str], list[str]]:
    """Score whether underlying price confirms the flow direction.

    Placeholder logic intended for MVP scaffolding.
    """
    score = 0.0
    reasons: list[str] = []
    risk_flags: list[str] = []

    if current_price is None:
        return 0.0, reasons, ["missing current price"]

    if vwap is not None:
        if direction == Direction.BULLISH and current_price >= vwap:
            score += 4
            reasons.append("price above VWAP")
        elif direction == Direction.BEARISH and current_price <= vwap:
            score += 4
            reasons.append("price below VWAP")
        else:
            risk_flags.append("price not confirming VWAP")

    if prior_high is not None and direction == Direction.BULLISH:
        if current_price > prior_high:
            score += 3
            reasons.append("price above prior high")

    if prior_low is not None and direction == Direction.BEARISH:
        if current_price < prior_low:
            score += 3
            reasons.append("price below prior low")

    return score, reasons, risk_flags
