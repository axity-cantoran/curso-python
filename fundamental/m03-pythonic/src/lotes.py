def generar_lotes(datos, tamaño):
    if isinstance(tamaño, bool) or not isinstance(tamaño, int):
        raise TypeError("El tamaño debe ser un entero")

    if tamaño <= 0:
        raise ValueError("El tamaño debe ser mayor que cero")

    for inicio in range(0, len(datos), tamaño):
        yield datos[inicio : inicio + tamaño]


if __name__ == "__main__":
    datos = list(range(1, 8))

    for lote in generar_lotes(datos, 3):
        print(lote)
