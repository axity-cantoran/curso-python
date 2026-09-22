# Módulo 06: Librería estándar y E/S

## Objetivo

Leer datos desde un archivo CSV, convertirlos a estructuras Python, calcular métricas, exportar los resultados a JSON y registrar el flujo mediante logging.

## Contenidos aplicados

- `pathlib`.
- Lectura de archivos.
- CSV mediante `csv.DictReader`.
- Conversión de tipos.
- Fechas con `datetime`.
- Zonas horarias con `timezone` y `zoneinfo`.
- Serialización JSON.
- Logging con distintos niveles.
- Manejo de errores.
- Automatización de validaciones de calidad.

## Estructura del proyecto

```text
m06-libreria-estandar-io/
├── .gitignore
├── .pre-commit-config.yaml
├── datos/
│   └── ventas.csv
├── logs/
├── salidas/
├── pyproject.toml
├── README.md
└── src/
    ├── exportacion.py
    ├── ingesta.py
    ├── main.py
    └── metricas.py
```

Las carpetas `logs/` y `salidas/` se utilizan durante la ejecución. Los archivos generados localmente se controlan mediante `.gitignore` según la configuración del proyecto.

## Archivo CSV

El archivo `datos/ventas.csv` contiene los campos:

- `fecha`
- `producto`
- `cantidad`
- `precio`

Ejemplo:

```csv
fecha,producto,cantidad,precio
2026-01-15T10:30:00+00:00,Teclado,2,50.0
```

Los valores leídos mediante `csv.DictReader` llegan inicialmente como cadenas y se convierten antes de procesarse:

- `fecha` → `datetime`.
- `cantidad` → `int`.
- `precio` → `float`.

## Ingesta de datos

El módulo `src/ingesta.py`:

- Construye rutas mediante `pathlib.Path`.
- Abre el CSV usando `encoding="utf-8"`.
- Lee cada fila con `csv.DictReader`.
- Convierte los valores al tipo correspondiente.
- Convierte las fechas mediante `datetime.fromisoformat`.
- Descarta filas inválidas.
- Registra advertencias para datos incorrectos.

Función principal:

```python
def leer_ventas(ruta: Path) -> list[dict[str, object]]:
    ...
```

## Métricas

El módulo `src/metricas.py` calcula:

- Cantidad de ventas.
- Unidades vendidas.
- Ingreso total.
- Producto con mayor ingreso.

El ingreso de cada fila se calcula como:

```text
ingreso = cantidad × precio
```

Con los datos iniciales, las métricas esperadas son:

```json
{
  "cantidad_ventas": 5,
  "unidades_vendidas": 9,
  "ingreso_total": 825.0,
  "producto_mayor_ingreso": "Monitor"
}
```

La estructura de las métricas se documenta mediante `TypedDict`.

## Exportación JSON

El módulo `src/exportacion.py`:

- Crea la carpeta de salida si no existe.
- Escribe las métricas en JSON.
- Utiliza codificación UTF-8.
- Aplica indentación para facilitar la lectura.
- Registra errores de escritura.
- Registra la exportación exitosa.

El resultado se guarda en:

```text
salidas/metricas.json
```

## Fechas y zonas horarias

Las fechas del CSV incluyen una zona horaria, por ejemplo:

```text
2026-01-15T10:30:00+00:00
```

El programa utiliza objetos `datetime` conscientes de zona horaria.

Buenas prácticas aplicadas:

- Recibir fechas con información de zona.
- Utilizar UTC como referencia.
- Evitar mezclar fechas naïve y aware.
- Convertir a una zona local solo cuando sea necesario mostrar la información.

## Logging

El módulo `src/main.py` configura logging para enviar mensajes a:

- La terminal.
- El archivo `logs/ventas.log`.

Se utiliza un formato que incluye:

- Fecha y hora.
- Nivel.
- Nombre del logger.
- Mensaje.

Niveles utilizados:

- `DEBUG`: detalle de filas procesadas.
- `INFO`: inicio, finalización y métricas.
- `WARNING`: filas descartadas por datos inválidos.
- `ERROR`: problemas de archivos o procesamiento.

Los errores capturados con una excepción se registran mediante `logger.exception`.

## Manejo de errores

Se probaron los siguientes casos:

- Archivo CSV inexistente.
- Cantidad no numérica.
- Precio no numérico.
- Fecha con formato inválido.
- Filas descartadas sin detener todo el procesamiento.
- Errores durante la escritura del JSON.

## Ejecución

Desde la raíz del proyecto:

```bash
poetry run python src/main.py
```

El programa:

1. Lee `datos/ventas.csv`.
2. Convierte y valida las filas.
3. Calcula las métricas.
4. Escribe `salidas/metricas.json`.
5. Registra el proceso en consola y en `logs/ventas.log`.


## Archivos generados localmente

El archivo `.gitignore` excluye las rutas generadas localmente, como:

```text
.venv/
.ruff_cache/
.pytest_cache/
.mypy_cache/
logs/
__pycache__/
*.py[cod]
```

## Resultado del laboratorio

Se implementó un flujo completo de ingesta y procesamiento:

- Lectura segura de rutas y archivos.
- Parseo de CSV.
- Conversión de datos.
- Manejo de fechas con zona horaria.
- Cálculo de métricas.
- Exportación a JSON.
- Logging en consola y archivo.
- Manejo de errores.
- Validación con herramientas de calidad.
- Automatización mediante pre-commit.