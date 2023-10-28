import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='API')
    SQLALCHEMY_DATABASE_URL: str = 'sqlite+aiosqlite://'


settings = Settings()
