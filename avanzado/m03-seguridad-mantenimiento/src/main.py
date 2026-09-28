import logging

from src.config import Settings

logger = logging.getLogger(__name__)


def configurar_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def validar_runtime(settings: Settings) -> None:
    if settings.app_env == "production":
        if settings.debug:
            raise RuntimeError("debug no puede estar activo en producción")

        if not settings.api_token:
            raise RuntimeError("Falta api_token en producción")


def main() -> None:
    # api_token se carga desde .env mediante pydantic-settings.
    settings = Settings()  # type: ignore[call-arg]

    validar_runtime(settings)
    configurar_logging(settings.log_level)

    logger.info(
        "Aplicación iniciada en entorno %s",
        settings.app_env,
    )

    print("Configuración válida")


if __name__ == "__main__":
    main()
