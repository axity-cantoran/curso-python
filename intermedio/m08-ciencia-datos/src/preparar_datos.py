from pathlib import Path
from typing import cast

import pandas as pd
from sklearn.model_selection import train_test_split

SplitResult = tuple[
    pd.DataFrame,
    pd.Series,
    pd.DataFrame,
    pd.Series,
]

COLUMNAS_REQUERIDAS = {
    "edad",
    "ingresos",
    "visitas",
    "compro",
}


def cargar_y_preparar_datos(
    ruta: Path,
) -> SplitResult:
    datos = pd.read_csv(ruta)

    columnas_faltantes = COLUMNAS_REQUERIDAS - set(datos.columns)

    if columnas_faltantes:
        raise ValueError(f"Faltan columnas: {columnas_faltantes}")

    datos = datos.dropna()

    X = datos[["edad", "ingresos", "visitas"]]
    y = datos["compro"]

    resultado = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    return cast(SplitResult, tuple(resultado))


# Prueba temporal
if __name__ == "__main__":
    ruta = Path("datos/clientes.csv")

    X_train, X_test, y_train, y_test = cargar_y_preparar_datos(ruta)

    print(f"X_train: {X_train.shape}")
    print(f"X_test: {X_test.shape}")
    print(f"y_train: {y_train.shape}")
    print(f"y_test: {y_test.shape}")
    print(y_train.value_counts())
    print(y_test.value_counts())
