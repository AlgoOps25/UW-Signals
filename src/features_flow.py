"""Flow feature calculations.

These helpers convert normalized options-flow events into directional evidence.
"""

from __future__ import annotations

from collections import defaultdict

from src.models import Direction, OptionFlowEvent, OptionSide


def estimate_direction(event: OptionFlowEvent) -> Direction:
    """Estimate event direction from option side and fill location.

    Final logic must be adjusted after confirming UW response fields.
    """
    if event.bid is None or event.ask is None or event.price is None or event.side is None:
        return Direction.MIXED

    midpoint = (event.bid + event.ask) / 2

    if event.side == OptionSide.CALL:
        return Direction.BULLISH if event.price >= midpoint else Direction.BEARISH

    if event.side == OptionSide.PUT:
        return Direction.BEARISH if event.price >= midpoint else Direction.BULLISH

    return Direction.MIXED


def premium_imbalance(events: list[OptionFlowEvent]) -> dict[str, float]:
    """Calculate bullish/bearish premium imbalance for a window."""
    bullish = 0.0
    bearish = 0.0

    for event in events:
        premium = float(event.premium or 0)
        direction = event.estimated_direction or estimate_direction(event)

        if direction == Direction.BULLISH:
            bullish += premium
        elif direction == Direction.BEARISH:
            bearish += premium

    total = bullish + bearish
    net = bullish - bearish
    ratio = bullish / bearish if bearish > 0 else float("inf") if bullish > 0 else 0.0

    return {
        "bullish_premium": bullish,
        "bearish_premium": bearish,
        "total_premium": total,
        "net_premium": net,
        "bull_bear_ratio": ratio,
    }


def strike_clusters(events: list[OptionFlowEvent]) -> dict[str, float]:
    """Aggregate premium by ticker/expiration/strike/side."""
    clusters: dict[str, float] = defaultdict(float)
    for event in events:
        if event.expiration is None or event.strike is None or event.side is None:
            continue
        key = f"{event.ticker}:{event.expiration}:{event.strike}:{event.side.value}"
        clusters[key] += float(event.premium or 0)
    return dict(clusters)
