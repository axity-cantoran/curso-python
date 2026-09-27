import warnings
from pathlib import Path

import joblib
from scipy.optimize import OptimizeWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.preparar_datos import cargar_y_preparar_datos

warnings.filterwarnings(
    "ignore",
    category=OptimizeWarning,
    message="Unknown solver options: iprint",
)


def entrenar_modelo(
    ruta_csv: Path,
    ruta_modelo: Path,
) -> float:
    X_train, X_test, y_train, y_test = cargar_y_preparar_datos(ruta_csv)

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    solver="lbfgs",
                    max_iter=1000,
                ),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)

    predicciones = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predicciones)

    ruta_modelo.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, ruta_modelo)

    return float(accuracy)


# Prueba temporal
if __name__ == "__main__":
    accuracy = entrenar_modelo(
        Path("datos/clientes.csv"),
        Path("modelos/clasificador.joblib"),
    )

    print(f"Accuracy: {accuracy:.2f}")
