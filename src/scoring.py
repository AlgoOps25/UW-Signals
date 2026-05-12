"""Opportunity scoring engine.

The scoring model mirrors the master roadmap:
- Directional flow: 25
- Market confirmation: 20
- Dealer/GEX context: 20
- Contract quality: 15
- Price action: 10
- Risk filter: 10
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.models import Direction, Regime
from src.risk_filters import RiskDecision


@dataclass
class ScoreBreakdown:
    directional_flow: float = 0.0
    market_confirmation: float = 0.0
    dealer_gex: float = 0.0
    contract_quality: float = 0.0
    price_action: float = 0.0
    risk_filter: float = 10.0
    reasons: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)

    @property
    def total(self) -> float:
        return max(
            0.0,
            min(
                100.0,
                self.directional_flow
                + self.market_confirmation
                + self.dealer_gex
                + self.contract_quality
                + self.price_action
                + self.risk_filter,
            ),
        )


def alert_band(score: float) -> str:
    """Map numeric score to alert band."""
    if score >= 90:
        return "apex"
    if score >= 85:
        return "strong"
    if score >= 78:
        return "watch"
    return "no_alert"


def score_opportunity(
    direction: Direction,
    regime: Regime,
    flow_score: float,
    market_score: float,
    gex_score: float,
    contract_score: float,
    price_score: float,
    risk_decision: RiskDecision | None = None,
    reasons: list[str] | None = None,
) -> ScoreBreakdown:
    """Combine component scores into a normalized opportunity score."""
    breakdown = ScoreBreakdown(
        directional_flow=min(max(flow_score, 0), 25),
        market_confirmation=min(max(market_score, 0), 20),
        dealer_gex=min(max(gex_score, 0), 20),
        contract_quality=min(max(contract_score, 0), 15),
        price_action=min(max(price_score, 0), 10),
        reasons=list(reasons or []),
    )

    breakdown.reasons.append(f"direction={direction.value}")
    breakdown.reasons.append(f"regime={regime.value}")

    if risk_decision is not None:
        breakdown.risk_flags.extend(risk_decision.flags)
        breakdown.risk_filter = max(0.0, 10.0 - risk_decision.score_penalty)
        if not risk_decision.allowed:
            breakdown.risk_filter = 0.0
            breakdown.risk_flags.append("blocked by risk filter")

    return breakdown
