from time import perf_counter

import httpx


def fetch_urls_sync(
    urls: list[str],
    timeout: float = 10.0,
) -> list[dict[str, object]]:
    resultados: list[dict[str, object]] = []

    with httpx.Client(timeout=timeout) as cliente:
        for url in urls:
            inicio = perf_counter()

            try:
                respuesta = cliente.get(url)
                respuesta.raise_for_status()

                resultados.append(
                    {
                        "url": url,
                        "status_code": respuesta.status_code,
                        "elapsed": perf_counter() - inicio,
                    }
                )
            except httpx.HTTPError as error:
                resultados.append(
                    {
                        "url": url,
                        "error": str(error),
                        "elapsed": perf_counter() - inicio,
                    }
                )

    return resultados


# Prueba temporal
if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://example.org",
    ]

    resultados = fetch_urls_sync(urls)

    for resultado in resultados:
        print(resultado)
