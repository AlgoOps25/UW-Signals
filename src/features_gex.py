"""GEX / dealer-context feature calculations.

This module will consume confirmed UW GEX / Greek Exposure responses after API access.
"""

from __future__ import annotations

from src.models import Regime


def classify_gex_regime(
    net_gex: float | None = None,
    spot_price: float | None = None,
    gamma_flip: float | None = None,
    distance_to_call_wall_pct: float | None = None,
    distance_to_put_wall_pct: float | None = None,
) -> Regime:
    """Classify market regime from dealer/GEX context.

    Placeholder rules. These must be tuned after live UW data is collected.
    """
    if net_gex is None:
        return Regime.UNKNOWN

    near_call_wall = distance_to_call_wall_pct is not None and distance_to_call_wall_pct < 0.25
    near_put_wall = distance_to_put_wall_pct is not None and distance_to_put_wall_pct < 0.25

    if net_gex > 0 and (near_call_wall or near_put_wall):
        return Regime.RANGE_PIN

    if net_gex < 0 and spot_price is not None and gamma_flip is not None:
        if spot_price > gamma_flip:
            return Regime.TREND_UP
        if spot_price < gamma_flip:
            return Regime.TREND_DOWN

    if net_gex < 0:
        return Regime.VOL_EXPANSION

    return Regime.UNKNOWN


def wall_distance_pct(spot_price: float, wall_price: float | None) -> float | None:
    """Calculate percentage distance from spot to a GEX wall."""
    if wall_price is None or spot_price <= 0:
        return None
    return abs(wall_price - spot_price) / spot_price * 100
