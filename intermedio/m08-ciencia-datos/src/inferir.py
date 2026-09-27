from pathlib import Path

import joblib
import pandas as pd

COLUMNAS_ENTRADA = [
    "edad",
    "ingresos",
    "visitas",
]


def realizar_inferencia(
    ruta_modelo: Path,
    datos: pd.DataFrame,
) -> list[int]:
    columnas_faltantes = set(COLUMNAS_ENTRADA) - set(datos.columns)

    if columnas_faltantes:
        raise ValueError(f"Faltan columnas: {columnas_faltantes}")

    entradas = datos[COLUMNAS_ENTRADA]

    if entradas.isna().any().any():
        raise ValueError("Los datos de inferencia contienen valores faltantes")

    modelo = joblib.load(ruta_modelo)
    predicciones = modelo.predict(entradas)

    return [int(prediccion) for prediccion in predicciones]


# Prueba temporal
if __name__ == "__main__":
    datos_nuevos = pd.DataFrame(
        [
            {
                "edad": 29,
                "ingresos": 2800,
                "visitas": 4,
            },
            {
                "edad": 48,
                "ingresos": 5000,
                "visitas": 8,
            },
        ]
    )

    predicciones = realizar_inferencia(
        Path("modelos/clasificador.joblib"),
        datos_nuevos,
    )

    print(f"Predicciones: {predicciones}")
