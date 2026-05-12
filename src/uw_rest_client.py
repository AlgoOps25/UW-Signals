"""Unusual Whales REST API client skeleton.

Official API docs: https://api.unusualwhales.com/docs
Base URL referenced by UW docs/examples: https://api.unusualwhales.com
Authentication: Authorization: Bearer <UW_API_KEY>
"""

from __future__ import annotations

from typing import Any

import httpx

from src.config import get_settings


class UWRestClient:
    """Thin REST client wrapper for Unusual Whales API calls."""

    def __init__(self, api_key: str | None = None, base_url: str = "https://api.unusualwhales.com") -> None:
        settings = get_settings()
        self.api_key = api_key or settings.uw_api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=30,
            headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Perform a GET request and return JSON."""
        response = self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self.client.close()

    def health_check(self) -> dict[str, Any]:
        """Placeholder API health check.

        Replace the path with a confirmed low-cost endpoint after API access is purchased.
        """
        return {"status": "not_implemented", "message": "Configure a confirmed UW endpoint after subscription."}
