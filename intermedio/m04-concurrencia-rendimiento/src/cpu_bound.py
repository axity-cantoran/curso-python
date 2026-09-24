from concurrent.futures import ProcessPoolExecutor
from time import perf_counter


def suma_de_cuadrados(limite: int) -> int:
    return sum(numero * numero for numero in range(limite))


def ejecutar_secuencial(
    limites: list[int],
) -> tuple[list[int], float]:
    inicio = perf_counter()
    resultados = [suma_de_cuadrados(limite) for limite in limites]
    duracion = perf_counter() - inicio

    return resultados, duracion


def ejecutar_con_procesos(
    limites: list[int],
) -> tuple[list[int], float]:
    inicio = perf_counter()

    with ProcessPoolExecutor() as executor:
        resultados = list(executor.map(suma_de_cuadrados, limites))

    duracion = perf_counter() - inicio

    return resultados, duracion


# Prueba temporal
if __name__ == "__main__":
    limites = [
        500_000,
        600_000,
        700_000,
        800_000,
    ]

    resultados_sync, tiempo_sync = ejecutar_secuencial(limites)
    resultados_process, tiempo_process = ejecutar_con_procesos(limites)

    print(f"Resultados secuenciales: {resultados_sync}")
    print(f"Resultados con procesos: {resultados_process}")
    print(f"Tiempo secuencial: {tiempo_sync:.4f} segundos")
    print(f"Tiempo con procesos: {tiempo_process:.4f} segundos")
