"""Risk filters and kill-switch rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time


@dataclass
class RiskDecision:
    allowed: bool = True
    flags: list[str] = field(default_factory=list)
    score_penalty: float = 0.0


def evaluate_basic_risk_filters(
    spread_pct: float | None = None,
    event_time: datetime | None = None,
    has_news_risk: bool = False,
    has_earnings_risk: bool = False,
    has_halt_risk: bool = False,
    recent_failed_same_direction_alerts: int = 0,
) -> RiskDecision:
    """Evaluate MVP risk filters.

    The goal is to block or downgrade weak/high-risk alerts before they reach the trader.
    """
    decision = RiskDecision()

    if spread_pct is None:
        decision.flags.append("missing spread data")
        decision.score_penalty += 2
    elif spread_pct > 12:
        decision.allowed = False
        decision.flags.append("spread too wide")
    elif spread_pct > 8:
        decision.flags.append("spread elevated")
        decision.score_penalty += 4

    if has_news_risk:
        decision.allowed = False
        decision.flags.append("headline/news risk")

    if has_earnings_risk:
        decision.allowed = False
        decision.flags.append("earnings risk")

    if has_halt_risk:
        decision.allowed = False
        decision.flags.append("halt risk")

    if recent_failed_same_direction_alerts >= 2:
        decision.allowed = False
        decision.flags.append("two recent failed same-direction alerts")

    if event_time is not None:
        # Placeholder: avoid very late 0DTE entries unless explicitly enabled later.
        if event_time.time() >= time(15, 30):
            decision.flags.append("late-day theta danger")
            decision.score_penalty += 5

    return decision
