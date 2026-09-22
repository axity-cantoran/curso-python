from contextlib import contextmanager
from time import perf_counter


@contextmanager
def medir_tiempo(nombre="Bloque"):
    inicio = perf_counter()

    try:
        yield
    finally:
        duracion = perf_counter() - inicio
        print(f"{nombre}: {duracion:.4f} segundos")


if __name__ == "__main__":
    with medir_tiempo("Procesamiento"):
        sum(range(1_000_000))


# Bloque de prueba con error
"""
if __name__ == "__main__":
    with medir_tiempo("Bloque con error"):
        raise ValueError("Error de prueba")
"""
