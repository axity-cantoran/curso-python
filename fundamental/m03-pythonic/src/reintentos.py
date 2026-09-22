from functools import wraps
from time import sleep


def reintentar(
    intentos=3,
    espera_inicial=0.5,
    factor_backoff=2,
    excepciones=(Exception,),  # Tupla al agregar ','
):
    if intentos < 1:
        raise ValueError("intentos debe ser mayor que cero")

    if espera_inicial < 0:
        raise ValueError("espera_inicial no puede ser negativa")

    if factor_backoff < 1:
        raise ValueError("factor_backoff debe ser mayor o igual que uno")

    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            espera = espera_inicial

            for intento in range(1, intentos + 1):
                try:
                    return funcion(*args, **kwargs)
                except excepciones:
                    if intento == intentos:
                        raise

                    print(
                        f"Intento {intento} fallido. "
                        f"Reintentando en {espera:.2f} segundos..."
                    )
                    sleep(espera)
                    espera *= factor_backoff

        return envoltura

    return decorador


# Función de prueba para demostrar el decorador
if __name__ == "__main__":
    llamadas = [0]

    @reintentar(intentos=3, espera_inicial=0.1)
    def operacion_inestable():
        llamadas[0] += 1

        if llamadas[0] < 3:
            raise RuntimeError("Fallo temporal")

        return "Operación exitosa"

    print(operacion_inestable())
