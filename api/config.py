from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Config(BaseSettings):
    SUPERUSER_EMAIL: str = Field(...)
    SUPERUSER_PASSWORD: str = Field(...)
    SUPERUSER_ID: str = Field(...)

    JWT_SECRET_KEY: str = Field(...)
    JWT_RESET_SECRET_KEY: str = Field(...)
    JWT_VERIFY_SECRET_KEY: str = Field(...)
    ALGORITHM: str = Field(...)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(...)
    RESET_TOKEN_EXPIRE_MINUTES: int = Field(...)
    VERIFY_TOKEN_EXPIRE_MINUTES: int = Field(...)

    GEMINI_API_KEY: str = Field(...)

    MONGO_USERNAME: str = Field(...)
    MONGO_PASSWORD: str = Field(...)
    MONGO_HOST: str = Field(...)
    MONGO_PORT: str = Field(...)
    MONGO_DB: str = Field(...)
    MONGO_URI: str = Field(...)


class DevConfig(Config):
    model_config = SettingsConfigDict(env_file="env/.env.dev", env_file_encoding="utf-8")


config: Config = DevConfig()
