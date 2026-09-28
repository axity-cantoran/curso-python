import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_url: str
    api_token: str | None
    timeout: float


def load_settings() -> Settings:
    api_url = os.getenv(
        "ORDERS_API_URL",
        "http://localhost:8000",
    )
    api_token = os.getenv("ORDERS_API_TOKEN")
    timeout = float(os.getenv("ORDERS_API_TIMEOUT", "10"))

    if not api_url.startswith(("http://", "https://")):
        raise ValueError("ORDERS_API_URL no es válida")

    if timeout <= 0:
        raise ValueError("ORDERS_API_TIMEOUT debe ser mayor que cero")

    return Settings(
        api_url=api_url.rstrip("/"),
        api_token=api_token,
        timeout=timeout,
    )
