# Módulo 08: Ciencia de datos

## Descripción

Este módulo implementa un flujo básico de ciencia de datos:

1. Carga de datos desde CSV.
2. Limpieza y validación con Pandas.
3. Preparación de variables predictoras y objetivo.
4. Entrenamiento de un clasificador.
5. Evaluación del modelo.
6. Serialización con `joblib`.
7. Inferencia sobre datos nuevos.

## Objetivos

- Manipular datos tabulares.
- Limpiar y validar información.
- Separar variables predictoras y objetivo.
- Entrenar un modelo clásico de clasificación.
- Evaluar resultados.
- Guardar y cargar un modelo.
- Realizar inferencias básicas.

## Dependencias

El módulo utiliza:

- NumPy.
- Pandas.
- Polars.
- scikit-learn `1.5.2`.
- joblib.

La versión de scikit-learn se fijó por compatibilidad con el entorno corporativo.

## Estructura del módulo

```text
m08-ciencia-datos/
├── datos/
│   └── clientes.csv
├── modelos/
│   └── clasificador.joblib
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── preparar_datos.py
│   ├── entrenar.py
│   ├── inferir.py
│   └── main.py
└── tests/
```

## Dataset

El archivo de entrada es:

```text
datos/clientes.csv
```

Contiene las columnas:

- `edad`.
- `ingresos`.
- `visitas`.
- `compro`.

La columna `compro` es la variable objetivo.

Las demás columnas son variables predictoras:

```text
edad
ingresos
visitas
```

## Pandas

Pandas se utiliza para:

- Leer el CSV.
- Inspeccionar los datos.
- Revisar tipos.
- Detectar valores faltantes.
- Separar variables predictoras y objetivo.

Ejemplo:

```python
datos = pd.read_csv("datos/clientes.csv")
```

## Polars

Polars se utilizó para comprobar la lectura de datos tabulares y comparar una alternativa eficiente a Pandas:

```python
datos = pl.read_csv("datos/clientes.csv")
```

El módulo se centra principalmente en Pandas para el flujo de entrenamiento.

## NumPy

NumPy se utilizó para comprobar operaciones numéricas vectorizadas:

```python
valores = np.array([1, 2, 3])
dobles = valores * 2
```

Las operaciones vectorizadas se aplican a todos los elementos sin escribir un bucle explícito.

## Preparación de datos

El módulo:

1. Lee el CSV.
2. Verifica las columnas requeridas.
3. Elimina filas con valores faltantes.
4. Separa `X` e `y`.
5. Divide los datos en entrenamiento y prueba.

Las variables predictoras son:

```python
X = datos[["edad", "ingresos", "visitas"]]
```

La variable objetivo es:

```python
y = datos["compro"]
```

La división utiliza:

```python
train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)
```

### `random_state`

Permite que la división sea reproducible. Con el mismo valor, las ejecuciones utilizan la misma separación entre entrenamiento y prueba.

### `stratify`

Conserva, en la medida posible, la proporción de clases en ambos conjuntos.

## Pipeline de scikit-learn

El entrenamiento utiliza un pipeline:

```python
Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression()),
])
```

El pipeline combina:

1. Escalado de variables numéricas.
2. Entrenamiento del clasificador.

Esto garantiza que el mismo preprocesamiento se aplique durante el entrenamiento y la inferencia.

## Clasificador

Se utiliza:

```python
LogisticRegression(
    solver="lbfgs",
    max_iter=1000,
)
```

El modelo aprende a clasificar los registros según las variables predictoras.

Entrenamiento:

```python
pipeline.fit(X_train, y_train)
```

Predicción:

```python
predicciones = pipeline.predict(X_test)
```

## Evaluación

La métrica utilizada es `accuracy`:

```python
accuracy = accuracy_score(
    y_test,
    predicciones,
)
```

La exactitud representa la proporción de predicciones correctas respecto al total de predicciones.

Con el dataset pequeño utilizado, se obtuvo:

```text
Accuracy: 1.00
```

Este resultado sirve para comprobar el flujo del laboratorio, pero no garantiza que el modelo generalice correctamente. Para una evaluación real se necesitarían más datos y métricas adicionales.

## Serialización con joblib

El pipeline entrenado se guarda en:

```text
modelos/clasificador.joblib
```

Guardar:

```python
joblib.dump(pipeline, ruta_modelo)
```

Cargar:

```python
modelo = joblib.load(ruta_modelo)
```

Guardar el pipeline completo permite conservar:

- Escalador.
- Modelo.
- Parámetros aprendidos.
- Orden de las transformaciones.

## Inferencia

La inferencia utiliza datos nuevos con las mismas columnas:

```python
datos_nuevos = pd.DataFrame([
    {
        "edad": 29,
        "ingresos": 2800,
        "visitas": 4,
    },
])
```

El modelo cargado genera predicciones:

```python
predicciones = modelo.predict(
    datos_nuevos[
        ["edad", "ingresos", "visitas"]
    ]
)
```

El resultado observado durante el laboratorio fue:

```text
Predicciones: [1, 1]
```

Las predicciones dependen del conjunto de datos, la división y el modelo entrenado.

## Validación de inferencia

Antes de predecir, se comprueba que existan las columnas requeridas:

```python
COLUMNAS_ENTRADA = [
    "edad",
    "ingresos",
    "visitas",
]
```

Si falta una columna, se genera:

```python
ValueError
```

También se validan valores faltantes. Si una columna contiene `NaN`, la inferencia se detiene con un mensaje controlado:

```text
Los datos de inferencia contienen valores faltantes
```

Esto evita que el error interno de scikit-learn llegue sin contexto al usuario.

## Advertencias y compatibilidad

Durante el entrenamiento apareció una advertencia relacionada con:

```text
Unknown solver options: iprint
```

La advertencia provino de la combinación de `scikit-learn==1.5.2` con dependencias numéricas del entorno. El entrenamiento funcionó correctamente y la advertencia se filtró de forma localizada mediante `OptimizeWarning`.

La versión `1.5.2` quedó fijada por compatibilidad con el equipo corporativo.

## Tipado estático y compatibilidad

Se utiliza mypy para revisar el código propio del módulo.

Algunas bibliotecas de ciencia de datos no proporcionan stubs completos o un marcador `py.typed`. Por ello, el `pyproject.toml` incluye overrides específicos para:

- `scikit-learn`.
- `joblib`.
- `scipy`.

La configuración mantiene `strict = true` para el código propio, pero ignora la ausencia de stubs en esas bibliotecas externas.

También se instaló `pandas-stubs` como dependencia de desarrollo para mejorar el análisis de los objetos Pandas.

El hook local de pre-commit utiliza explícitamente:

```text
--config-file=intermedio/m08-ciencia-datos/pyproject.toml

## Ejecución

Desde la raíz del módulo:

```bash
poetry run python -m src.entrenar
```

Para ejecutar la inferencia:

```bash
poetry run python -m src.inferir
```

Para ejecutar el flujo completo:

```bash
poetry run python -m src.main
```

## Archivos generados

El modelo serializado se genera en:

```text
modelos/clasificador.joblib
```

Este archivo es un artefacto local de entrenamiento. Puede excluirse del repositorio si se desea reproducirlo mediante el script de entrenamiento.

## Resultado del módulo

Se implementó un flujo completo de ciencia de datos que:

- Lee datos con Pandas.
- Comprueba datos con Polars y NumPy.
- Limpia valores faltantes.
- Separa variables predictoras y objetivo.
- Divide los datos de forma reproducible.
- Entrena un clasificador mediante un pipeline.
- Evalúa el modelo con `accuracy`.
- Serializa el pipeline con `joblib`.
- Carga el modelo.
- Realiza inferencia con datos nuevos.
- Valida columnas y valores faltantes.