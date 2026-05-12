"""Alert delivery helpers for Discord/Telegram/email style outputs."""

from __future__ import annotations

import httpx

from src.config import get_settings
from src.models import SignalAlert
from src.scoring import alert_band


def format_alert_message(alert: SignalAlert) -> str:
    """Format a human-readable alert message."""
    band = alert_band(alert.score).upper()
    lines = [
        f"🚨 {alert.title} — {alert.score:.1f}/100 [{band}]",
        "",
        f"Ticker: {alert.ticker}",
        f"Direction: {alert.direction.value}",
        f"Regime: {alert.regime.value}",
        f"Action: {alert.action}",
    ]

    if alert.contract is not None:
        c = alert.contract
        lines.extend(
            [
                "",
                "Contract:",
                f"{c.ticker} {c.expiration} {c.strike}{c.side.value.upper()}",
            ]
        )

    if alert.reasons:
        lines.append("")
        lines.append("Why:")
        lines.extend(f"- {reason}" for reason in alert.reasons)

    if alert.invalidation:
        lines.append("")
        lines.append("Invalidation:")
        lines.extend(f"- {item}" for item in alert.invalidation)

    return "\n".join(lines)


def send_discord_alert(alert: SignalAlert, webhook_url: str | None = None) -> bool:
    """Send an alert to Discord using a webhook."""
    settings = get_settings()
    url = webhook_url or settings.discord_webhook_url
    if not url:
        return False

    payload = {"content": format_alert_message(alert)}
    response = httpx.post(url, json=payload, timeout=15)
    response.raise_for_status()
    return True
