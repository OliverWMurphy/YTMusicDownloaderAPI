from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    creator: str = "Oliver"
    model_config = SettingsConfigDict(env_file=".env",extra="allow")

@lru_cache
def get_settings():
    return Settings()
