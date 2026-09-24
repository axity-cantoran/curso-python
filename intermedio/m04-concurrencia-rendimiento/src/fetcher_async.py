import asyncio
from time import perf_counter

import httpx


async def fetch_one(
    cliente: httpx.AsyncClient,
    url: str,
    semaforo: asyncio.Semaphore,
) -> dict[str, object]:
    async with semaforo:
        inicio = perf_counter()

        try:
            respuesta = await cliente.get(url)
            respuesta.raise_for_status()

            return {
                "url": url,
                "status_code": respuesta.status_code,
                "elapsed": perf_counter() - inicio,
            }
        except httpx.HTTPError as error:
            return {
                "url": url,
                "error": str(error),
                "elapsed": perf_counter() - inicio,
            }


async def fetch_urls_async(
    urls: list[str],
    limite_concurrencia: int = 5,
    timeout: float = 10.0,
) -> list[dict[str, object]]:
    semaforo = asyncio.Semaphore(limite_concurrencia)
    limites_timeout = httpx.Timeout(timeout)

    async with httpx.AsyncClient(
        timeout=limites_timeout,
    ) as cliente:
        tareas = [fetch_one(cliente, url, semaforo) for url in urls]

        return await asyncio.gather(*tareas)


# Prueba temporal
if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://example.org",
        "https://www.python.org",
    ]

    resultados = asyncio.run(
        fetch_urls_async(
            urls,
            limite_concurrencia=2,
        )
    )

    for resultado in resultados:
        print(resultado)
