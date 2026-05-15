"""Parse Unusual Whales Discord bot/custom-alert messages.

The Server plan provides Discord posts rather than API JSON. This parser is
intentionally defensive: it stores raw messages and extracts best-effort fields
from content and embed text.
"""

from __future__ import annotations

import re
from typing import Any

from src.config import get_settings

CONTRACT_RE = re.compile(
    r"(?P<ticker>\$?[A-Z]{1,6})\s+"
    r"(?P<expiration>\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)\s+"
    r"(?P<strike>\d+(?:\.\d+)?)\s*"
    r"(?P<side>[CP])\b",
    re.IGNORECASE,
)

ALT_CONTRACT_RE = re.compile(
    r"(?P<ticker>\$?[A-Z]{1,6}).{0,30}?"
    r"(?P<strike>\d+(?:\.\d+)?)\s*"
    r"(?P<side>CALL|PUT|Calls?|Puts?)\b",
    re.IGNORECASE | re.DOTALL,
)

MONEY_RE = re.compile(r"\$\s?(?P<num>\d+(?:\.\d+)?)(?P<suffix>[KMB])?", re.IGNORECASE)
DTE_RE = re.compile(r"(?P<dte>\d+)\s*DTE", re.IGNORECASE)
PERCENT_RE = re.compile(r"(?P<num>\d+(?:\.\d+)?)\s*%")

FIELD_ALIASES = {
    "premium": ["premium", "prem"],
    "volume": ["volume", "vol"],
    "open_interest": ["open interest", "oi"],
    "volume_oi_ratio": ["volume / oi", "vol/oi", "volume/oi", "vol oi"],
    "spread": ["spread"],
    "bid": ["bid"],
    "ask": ["ask"],
    "spot": ["spot", "underlying", "stock price"],
    "iv": ["iv", "implied volatility"],
    "delta": ["delta"],
    "theta": ["theta"],
    "bullish_premium_pct": ["bullish prem", "bullish premium"],
    "bearish_premium_pct": ["bearish prem", "bearish premium"],
}


def _money_to_float(raw: str) -> float | None:
    match = MONEY_RE.search(raw or "")
    if not match:
        return None
    value = float(match.group("num"))
    suffix = (match.group("suffix") or "").upper()
    if suffix == "K":
        value *= 1_000
    elif suffix == "M":
        value *= 1_000_000
    elif suffix == "B":
        value *= 1_000_000_000
    return value


def _number_from_text(raw: str) -> float | None:
    cleaned = (raw or "").replace(",", "")
    money = _money_to_float(cleaned)
    if money is not None:
        return money
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(match.group(0)) if match else None


def flatten_embed(embed: dict[str, Any]) -> str:
    """Flatten a Discord embed dict into searchable text."""
    parts: list[str] = []
    for key in ("title", "description", "url"):
        value = embed.get(key)
        if value:
            parts.append(str(value))
    for field in embed.get("fields", []) or []:
        name = field.get("name", "")
        value = field.get("value", "")
        parts.append(f"{name}: {value}")
    footer = embed.get("footer") or {}
    if footer.get("text"):
        parts.append(str(footer["text"]))
    return "\n".join(parts)


def flatten_message(content: str | None, embeds: list[dict[str, Any]]) -> str:
    """Flatten content and embeds into one parseable text blob."""
    parts = [content or ""]
    parts.extend(flatten_embed(embed) for embed in embeds)
    return "\n".join(part for part in parts if part).strip()


def _extract_known_fields_from_embed(embed: dict[str, Any]) -> dict[str, Any]:
    extracted: dict[str, Any] = {}
    for field in embed.get("fields", []) or []:
        name = str(field.get("name", "")).strip().lower()
        value = str(field.get("value", "")).strip()
        for output_name, aliases in FIELD_ALIASES.items():
            if any(alias in name for alias in aliases):
                if output_name.endswith("pct"):
                    pct_match = PERCENT_RE.search(value)
                    extracted[output_name] = float(pct_match.group("num")) if pct_match else _number_from_text(value)
                else:
                    extracted[output_name] = _number_from_text(value)
    return extracted


def parse_uw_discord_message(content: str | None, embeds: list[dict[str, Any]]) -> dict[str, Any]:
    """Best-effort parser for UW Discord posts.

    Returns a dict that is safe to store even when most fields are unknown.
    """
    settings = get_settings()
    text = flatten_message(content, embeds)
    upper_text = text.upper()

    parsed: dict[str, Any] = {
        "source": "discord_uw_bot",
        "raw_text": text,
        "symbols": [],
        "contracts": [],
        "direction_hint": "unknown",
        "event_type": "unknown",
        "confidence": 0,
        "parser_warnings": [],
    }

    for symbol in settings.all_symbol_list:
        if re.search(rf"\b\$?{re.escape(symbol)}\b", upper_text):
            parsed["symbols"].append(symbol)

    for regex in (CONTRACT_RE, ALT_CONTRACT_RE):
        for match in regex.finditer(text):
            side_raw = match.group("side").upper()
            side = "call" if side_raw.startswith("C") else "put"
            contract = {
                "ticker": match.group("ticker").replace("$", "").upper(),
                "strike": float(match.group("strike")),
                "side": side,
            }
            if "expiration" in match.groupdict():
                contract["expiration"] = match.group("expiration")
            if contract not in parsed["contracts"]:
                parsed["contracts"].append(contract)

    dte_match = DTE_RE.search(text)
    if dte_match:
        parsed["dte"] = int(dte_match.group("dte"))

    extracted_fields: dict[str, Any] = {}
    for embed in embeds:
        extracted_fields.update(_extract_known_fields_from_embed(embed))
    parsed.update(extracted_fields)

    if "FLOW ALERT" in upper_text or "FLOW" in upper_text:
        parsed["event_type"] = "flow"
    if "LIVE OPTIONS FLOW" in upper_text:
        parsed["event_type"] = "live_options_flow"
    if "MARKET" in upper_text and "UPDATE" in upper_text:
        parsed["event_type"] = "market_update"
    if "ECONOMIC" in upper_text or "FOMC" in upper_text or "CPI" in upper_text:
        parsed["event_type"] = "macro_risk"
    if "HALT" in upper_text or "UNHALT" in upper_text:
        parsed["event_type"] = "halt_update"

    bullish_terms = ["BULLISH", "CALL", "ASK SIDE CALL", "BOUGHT CALL"]
    bearish_terms = ["BEARISH", "PUT", "ASK SIDE PUT", "BOUGHT PUT"]
    bullish_hits = sum(1 for term in bullish_terms if term in upper_text)
    bearish_hits = sum(1 for term in bearish_terms if term in upper_text)

    if bullish_hits > bearish_hits:
        parsed["direction_hint"] = "bullish"
    elif bearish_hits > bullish_hits:
        parsed["direction_hint"] = "bearish"
    elif bullish_hits or bearish_hits:
        parsed["direction_hint"] = "mixed"

    if parsed["symbols"]:
        parsed["confidence"] += 20
    if parsed["contracts"]:
        parsed["confidence"] += 30
    if parsed.get("premium") is not None:
        parsed["confidence"] += 15
    if parsed.get("volume") is not None or parsed.get("volume_oi_ratio") is not None:
        parsed["confidence"] += 15
    if parsed.get("dte") is not None:
        parsed["confidence"] += 10
    if parsed["direction_hint"] != "unknown":
        parsed["confidence"] += 10

    if not parsed["symbols"] and parsed["contracts"]:
        parsed["symbols"] = sorted({c["ticker"] for c in parsed["contracts"]})

    if not parsed["symbols"]:
        parsed["parser_warnings"].append("no approved symbol detected")
    if not parsed["contracts"]:
        parsed["parser_warnings"].append("no option contract detected")

    return parsed
