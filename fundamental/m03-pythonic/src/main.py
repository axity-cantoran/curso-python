from lotes import generar_lotes
from reintentos import reintentar
from temporizador import medir_tiempo

intentos_realizados = 0


# Caso Inicial con variable global (error)
@reintentar(
    intentos=3,
    espera_inicial=0.1,
    factor_backoff=2,
    excepciones=(RuntimeError,),
)
def procesar_lote(lote):
    global intentos_realizados

    intentos_realizados += 1

    if intentos_realizados == 1:
        raise RuntimeError("Fallo temporal al procesar el lote")

    return f"Lote procesado: {lote}"


def main():
    datos = list(range(1, 11))

    with medir_tiempo("Procesamiento total"):
        for lote in generar_lotes(datos, 3):
            print(procesar_lote(lote))


if __name__ == "__main__":
    main()
