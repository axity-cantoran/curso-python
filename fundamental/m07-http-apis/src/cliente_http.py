import logging
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Any, TypeVar

import httpx

logger = logging.getLogger(__name__)
Resultado = TypeVar("Resultado")


TIMEOUT = httpx.Timeout(
    connect=5.0,
    read=10.0,
    write=10.0,
    pool=5.0,
)


class ErrorHTTPReintentable(Exception):
    pass


def validar_respuesta(respuesta: httpx.Response) -> httpx.Response:
    if respuesta.status_code == 429 or respuesta.status_code >= 500:
        raise ErrorHTTPReintentable(f"Respuesta HTTP temporal: {respuesta.status_code}")

    respuesta.raise_for_status()
    return respuesta


@contextmanager
def crear_cliente() -> Iterator[httpx.Client]:
    cliente = httpx.Client(
        http2=True,
        timeout=TIMEOUT,
        headers={"User-Agent": "curso-python-m07"},
    )

    try:
        yield cliente
    finally:
        cliente.close()
        logger.debug("Cliente HTTP cerrado")


def con_reintentos(
    intentos: int = 3,
    espera_inicial: float = 0.5,
    factor_backoff: float = 2.0,
) -> Callable[[Callable[..., Resultado]], Callable[..., Resultado]]:
    if intentos < 1:
        raise ValueError("intentos debe ser mayor que cero")

    if espera_inicial < 0:
        raise ValueError("espera_inicial no puede ser negativa")

    if factor_backoff < 1:
        raise ValueError("factor_backoff debe ser mayor o igual que uno")

    def decorador(
        funcion: Callable[..., Resultado],
    ) -> Callable[..., Resultado]:
        @wraps(funcion)
        def envoltura(*args: object, **kwargs: object) -> Resultado:
            espera = espera_inicial

            for intento in range(1, intentos + 1):
                try:
                    return funcion(*args, **kwargs)
                except (
                    httpx.TimeoutException,
                    httpx.ConnectError,
                    ErrorHTTPReintentable,
                ) as error:
                    if intento == intentos:
                        raise

                    logger.warning(
                        "Intento %s fallido: %s. Reintentando en %.2f segundos",
                        intento,
                        error,
                        espera,
                    )
                    time.sleep(espera)
                    espera *= factor_backoff

            raise RuntimeError("No se pudo completar la operación")

        return envoltura

    return decorador


@con_reintentos(intentos=3, espera_inicial=0.5)
def realizar_get(
    cliente: httpx.Client,
    url: str,
    parametros: dict[str, Any] | None = None,
) -> httpx.Response:
    logger.info("Realizando GET a %s", url)

    respuesta = cliente.get(url, params=parametros)
    validar_respuesta(respuesta)

    logger.info(
        "Respuesta recibida: status=%s, version=%s",
        respuesta.status_code,
        respuesta.http_version,
    )

    return respuesta


# Prueba temporal
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    with crear_cliente() as cliente:
        respuesta = realizar_get(cliente, "https://example.com")
        print(respuesta.status_code)
