"""Unusual Whales WebSocket client skeleton.

Use this after confirming which WebSocket channels are included in API Advanced.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from typing import Any

import websockets

from src.config import get_settings


class UWWebSocketClient:
    """Minimal reconnect-capable WebSocket client scaffold."""

    def __init__(self, api_key: str | None = None, url: str = "") -> None:
        settings = get_settings()
        self.api_key = api_key or settings.uw_api_key
        self.url = url

    async def connect(self) -> AsyncIterator[str]:
        """Yield raw WebSocket messages.

        Set `self.url` to the confirmed UW WebSocket URL/channel after subscription.
        """
        if not self.url:
            raise ValueError("WebSocket URL is not configured yet.")

        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
        async with websockets.connect(self.url, extra_headers=headers) as websocket:
            async for message in websocket:
                yield message

    async def run_forever(
        self,
        handler: Callable[[str], Any],
        reconnect_delay_seconds: int = 5,
    ) -> None:
        """Run the WebSocket loop forever with basic reconnect handling."""
        while True:
            try:
                async for message in self.connect():
                    result = handler(message)
                    if asyncio.iscoroutine(result):
                        await result
            except Exception:
                await asyncio.sleep(reconnect_delay_seconds)
