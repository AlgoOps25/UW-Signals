"""Option contract quality calculations."""

from __future__ import annotations

from src.models import ContractCandidate


def calculate_spread_pct(bid: float | None, ask: float | None) -> float | None:
    """Return bid/ask spread as a percentage of midpoint."""
    if bid is None or ask is None or bid < 0 or ask <= 0:
        return None
    midpoint = (bid + ask) / 2
    if midpoint <= 0:
        return None
    return (ask - bid) / midpoint * 100


def score_contract_quality(candidate: ContractCandidate) -> tuple[float, list[str], list[str]]:
    """Score liquidity/risk quality for an option contract.

    Placeholder model. Thresholds must be tuned after live UW data is collected.
    """
    score = 0.0
    reasons: list[str] = []
    risk_flags: list[str] = []

    if candidate.spread_pct is not None:
        if candidate.spread_pct <= 5:
            score += 5
            reasons.append("tight spread")
        elif candidate.spread_pct <= 10:
            score += 3
            reasons.append("acceptable spread")
        else:
            risk_flags.append("wide spread")

    if candidate.volume is not None:
        if candidate.volume >= 1000:
            score += 4
            reasons.append("strong volume")
        elif candidate.volume >= 250:
            score += 2
            reasons.append("usable volume")
        else:
            risk_flags.append("low volume")

    if candidate.open_interest is not None:
        if candidate.open_interest >= 1000:
            score += 3
            reasons.append("strong open interest")
        elif candidate.open_interest < 100:
            risk_flags.append("low open interest")

    if candidate.delta is not None:
        abs_delta = abs(candidate.delta)
        if 0.25 <= abs_delta <= 0.65:
            score += 3
            reasons.append("usable delta range")
        else:
            risk_flags.append("delta outside preferred range")

    return score, reasons, risk_flags
