from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Config(BaseSettings):
    SUPERUSER_EMAIL: str = Field(...)
    SUPERUSER_PASSWORD: str = Field(...)

class DevConfig(Config):
    model_config = SettingsConfigDict(env_file="env/.env.dev", env_file_encoding="utf-8")


config: Config = DevConfig()
