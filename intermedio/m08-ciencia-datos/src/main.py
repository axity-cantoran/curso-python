from pathlib import Path

import pandas as pd

from src.entrenar import entrenar_modelo
from src.inferir import realizar_inferencia

RUTA_CSV = Path("datos/clientes.csv")
RUTA_MODELO = Path("modelos/clasificador.joblib")


def main() -> None:
    accuracy = entrenar_modelo(
        RUTA_CSV,
        RUTA_MODELO,
    )

    print(f"Accuracy: {accuracy:.2f}")

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
        RUTA_MODELO,
        datos_nuevos,
    )

    print(f"Predicciones: {predicciones}")


if __name__ == "__main__":
    main()
