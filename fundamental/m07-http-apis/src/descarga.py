import logging
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import ParamSpec, TypeVar

import httpx

from cliente_http import ErrorHTTPReintentable, validar_respuesta

logger = logging.getLogger(__name__)

Resultado = TypeVar("Resultado")
Parametros = ParamSpec("Parametros")


@contextmanager
def archivo_temporal(destino: Path) -> Iterator[Path]:
    temporal = destino.with_name(f"{destino.name}.part")
    temporal.parent.mkdir(parents=True, exist_ok=True)

    try:
        yield temporal
    except Exception:
        temporal.unlink(missing_ok=True)
        raise
    else:
        temporal.replace(destino)


def reintentar_descarga(
    intentos: int = 3,
    espera_inicial: float = 0.5,
    factor_backoff: float = 2.0,
) -> Callable[
    [
        Callable[
            Parametros,
            Resultado,
        ]
    ],
    Callable[
        Parametros,
        Resultado,
    ],
]:
    def decorador(
        funcion: Callable[Parametros, Resultado],
    ) -> Callable[Parametros, Resultado]:
        @wraps(funcion)
        def envoltura(
            *args: Parametros.args,
            **kwargs: Parametros.kwargs,
        ) -> Resultado:
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
                        "Descarga fallida en intento %s: %s. "
                        "Reintentando en %.2f segundos",
                        intento,
                        error,
                        espera,
                    )
                    time.sleep(espera)
                    espera *= factor_backoff

            raise RuntimeError("No se pudo completar la descarga")

        return envoltura

    return decorador


@reintentar_descarga(intentos=3, espera_inicial=0.5)
def descargar_stream(
    cliente: httpx.Client,
    url: str,
    destino: Path,
    tamaño_bloque: int = 64 * 1024,
) -> Path:
    logger.info("Iniciando descarga desde %s", url)

    with cliente.stream("GET", url) as respuesta:
        validar_respuesta(respuesta)

        with archivo_temporal(destino) as temporal:
            with temporal.open("wb") as archivo:
                for bloque in respuesta.iter_bytes(chunk_size=tamaño_bloque):
                    archivo.write(bloque)

    logger.info("Descarga finalizada: %s", destino)
    return destino


# Prueba temporal
if __name__ == "__main__":
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    from cliente_http import crear_cliente

    destino = Path("descargas") / "ejemplo.bin"

    with crear_cliente() as cliente:
        descargar_stream(
            cliente,
            "https://example.com",
            destino,
        )
