from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    service_url: str = "http://localhost:8000"
    api_token: str
    debug: bool = False
    timeout: float = Field(default=10.0, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
