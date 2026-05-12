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


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
