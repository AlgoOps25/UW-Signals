"""Typed data models for UW-Signals.

These models intentionally start vendor-neutral. After UW API access is purchased,
map confirmed response fields into these normalized structures.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Direction(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class Regime(str, Enum):
    TREND_UP = "trend_up"
    TREND_DOWN = "trend_down"
    RANGE_PIN = "range_pin"
    VOL_EXPANSION = "vol_expansion"
    CAUTION = "caution"
    UNKNOWN = "unknown"


class OptionSide(str, Enum):
    CALL = "call"
    PUT = "put"


class OptionFlowEvent(BaseModel):
    timestamp: datetime
    ticker: str
    expiration: str | None = None
    strike: float | None = None
    side: OptionSide | None = None
    estimated_direction: Direction = Direction.UNKNOWN if hasattr(Direction, "UNKNOWN") else Direction.MIXED
    premium: float | None = None
    size: int | None = None
    price: float | None = None
    bid: float | None = None
    ask: float | None = None
    volume: int | None = None
    open_interest: int | None = None
    implied_volatility: float | None = None
    dte: int | None = None
    raw: dict = Field(default_factory=dict)


class ContractCandidate(BaseModel):
    ticker: str
    expiration: str
    strike: float
    side: OptionSide
    score: float = 0.0
    spread_pct: float | None = None
    volume: int | None = None
    open_interest: int | None = None
    delta: float | None = None
    gamma: float | None = None
    theta: float | None = None
    vega: float | None = None
    reasons: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)


class SignalAlert(BaseModel):
    timestamp: datetime
    title: str
    ticker: str
    direction: Direction
    regime: Regime
    score: float
    contract: ContractCandidate | None = None
    reasons: list[str] = Field(default_factory=list)
    invalidation: list[str] = Field(default_factory=list)
    action: str = "watch"
