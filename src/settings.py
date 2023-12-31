from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='API_')
    DATABASE_URL: str = 'sqlite+aiosqlite:///main.db'
    SYNC_DATABASE_URL: str = 'sqlite:///main.db'


@cache
def settings():
    return Settings()
