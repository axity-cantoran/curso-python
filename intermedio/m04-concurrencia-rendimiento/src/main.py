import asyncio
from time import perf_counter

from src.cpu_bound import (
    ejecutar_con_procesos,
    ejecutar_secuencial,
)
from src.fetcher_async import fetch_urls_async
from src.fetcher_sync import fetch_urls_sync

URLS = [
    "https://example.com",
    "https://example.org",
    "https://www.python.org",
]


def medir_sincrono() -> tuple[list[dict[str, object]], float]:
    inicio = perf_counter()
    resultados = fetch_urls_sync(URLS)
    duracion = perf_counter() - inicio
    return resultados, duracion


async def medir_asincrono() -> tuple[
    list[dict[str, object]],
    float,
]:
    inicio = perf_counter()
    resultados = await fetch_urls_async(
        URLS,
        limite_concurrencia=2,
    )
    duracion = perf_counter() - inicio
    return resultados, duracion


def main() -> None:
    resultados_sync, tiempo_sync = medir_sincrono()
    resultados_async, tiempo_async = asyncio.run(medir_asincrono())

    limites = [
        500_000,
        600_000,
        700_000,
        800_000,
    ]

    resultados_sync, tiempo_cpu_sync = ejecutar_secuencial(limites)
    resultados_process, tiempo_cpu_process = ejecutar_con_procesos(limites)

    print(f"Tiempo síncrono: {tiempo_sync:.4f} segundos")
    print(f"Tiempo asíncrono: {tiempo_async:.4f} segundos")

    print(f"Tiempo CPU secuencial: {tiempo_cpu_sync:.4f} segundos")
    print(f"Tiempo CPU con procesos: {tiempo_cpu_process:.4f} segundos")

    print(
        "Resultados CPU iguales:",
        resultados_sync == resultados_process,
    )

    print(f"Resultados síncronos: {resultados_sync}")
    print(f"Resultados asíncronos: {resultados_async}")


if __name__ == "__main__":
    main()
