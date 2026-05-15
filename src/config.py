"""Configuration helpers for UW-Signals.

Real secrets should be loaded from environment variables or a local .env file.
Never commit API keys.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    uw_api_key: str = ""
    app_env: str = "local"
    database_url: str = "sqlite:///data/uw_signals.sqlite3"
    log_level: str = "INFO"
    summary_interval_seconds: int = 300

    discord_bot_token: str = ""
    discord_guild_id: str = ""
    discord_listen_channel_ids: str = ""
    discord_summary_channel_id: str = ""

    discord_webhook_url: str = ""
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    index_symbols: str = "SPX,SPY,QQQ,IWM"
    stock_symbols: str = "TSLA,NVDA,AAPL,AMD,META,MSFT,AMZN"

    @property
    def index_symbol_list(self) -> list[str]:
        return [s.strip().upper() for s in self.index_symbols.split(",") if s.strip()]

    @property
    def stock_symbol_list(self) -> list[str]:
        return [s.strip().upper() for s in self.stock_symbols.split(",") if s.strip()]

    @property
    def all_symbol_list(self) -> list[str]:
        return list(dict.fromkeys([*self.index_symbol_list, *self.stock_symbol_list]))

    @property
    def discord_listen_channel_id_list(self) -> list[int]:
        return [int(c.strip()) for c in self.discord_listen_channel_ids.split(",") if c.strip()]

    @property
    def discord_summary_channel_id_int(self) -> int | None:
        return int(self.discord_summary_channel_id) if self.discord_summary_channel_id.strip() else None


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
