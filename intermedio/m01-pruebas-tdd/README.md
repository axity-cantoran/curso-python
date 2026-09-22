# Módulo 01: Pruebas y TDD

## Descripción

Este módulo implementa una historia de negocio mediante **Test-Driven Development (TDD)**. Se utilizaron pruebas unitarias, fixtures, parametrización, markers, mocking, property-based testing y cobertura.

## Historia implementada

> Como usuario, quiero consultar un resumen de ventas para conocer el total y la cantidad de productos procesados.

## Criterios de aceptación

- Una lista vacía devuelve cantidad `0` e ingreso total `0.0`.
- Las ventas válidas se agregan correctamente.
- Las cantidades deben ser mayores que cero.
- Los precios deben ser mayores que cero.
- Los valores inválidos producen `ValueError`.
- Una fuente externa puede simularse mediante un mock.
- Las propiedades principales se verifican con Hypothesis.
- La suite genera un reporte de cobertura.
- CI ejecuta las pruebas y comprueba el umbral configurado.

## Estructura del proyecto

```text
m01-pruebas-tdd/
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
├── .pre-commit-config.yaml
├── poetry.lock
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   └── ventas.py
└── tests/
    ├── conftest.py
    ├── test_propiedades.py
    └── test_ventas.py
```

## Implementación

### `generar_resumen`

La función:

```python
def generar_resumen(ventas: list[Venta]) -> Resumen:
    ...
```

realiza lo siguiente:

- Cuenta las ventas.
- Valida cantidades.
- Valida precios.
- Calcula el ingreso total.
- Devuelve un resumen tipado.

El resultado contiene:

```python
{
    "cantidad_ventas": int,
    "ingreso_total": float,
}
```

### `obtener_ventas_desde_fuente`

La función:

```python
def obtener_ventas_desde_fuente(
    fuente: FuenteVentas,
) -> list[Venta]:
    ...
```

delega la obtención de ventas en una dependencia externa compatible con el protocolo `FuenteVentas`.

## Desarrollo mediante TDD

La implementación siguió el ciclo:

```text
Red → Green → Refactor
```

- **Red:** se escribió una prueba que fallaba.
- **Green:** se implementó el código mínimo para hacerla pasar.
- **Refactor:** se mejoró el código conservando el comportamiento probado.

El desarrollo comenzó con el caso de una lista vacía y después se agregaron ventas válidas y validaciones de errores.

## Fixtures

El archivo `tests/conftest.py` contiene la fixture:

```python
@pytest.fixture
def ventas_validas() -> list[Venta]:
    ...
```

La fixture proporciona datos reutilizables para varias pruebas.

## Parametrización

Se utilizó `pytest.mark.parametrize` para probar distintos valores inválidos sin duplicar la prueba:

```python
@pytest.mark.parametrize(
    "venta_invalida",
    [
        ...,
    ],
)
```

Se verificaron cantidades y precios:

- Iguales a cero.
- Negativos.

Todos estos casos deben producir `ValueError`.

## Markers

Se configuró el marker:

```text
unit
```

Ejecutar únicamente las pruebas unitarias:

```bash
poetry run pytest -m unit -q
```

Excluirlas:

```bash
poetry run pytest -m "not unit" -q
```

## Mocking

Se utilizó `unittest.mock.Mock` para sustituir una fuente externa de ventas.

Se configuró un resultado controlado mediante:

```python
fuente.obtener_ventas.return_value = [...]
```

También se simuló un error mediante:

```python
fuente.obtener_ventas.side_effect = ConnectionError(...)
```

Se verificó que la dependencia:

- Se llamara exactamente una vez.
- Recibiera los argumentos esperados.
- Devolviera los datos definidos.
- Propagara correctamente una excepción.

## Property-based testing

Se utilizó Hypothesis para generar listas de ventas automáticamente.

La prueba basada en propiedades verifica que:

- La cantidad de ventas coincida con la longitud de la lista.
- El ingreso total sea mayor o igual que cero.
- Se procesen listas de diferentes tamaños.
- Se contemplen cantidades y precios dentro de rangos válidos.

Ejecutar la prueba de propiedades:

```bash
poetry run pytest tests/test_propiedades.py -q
```

Hypothesis puede generar:

- Listas vacías.
- Una o varias ventas.
- Cantidades diferentes.
- Precios decimales.
- Casos cercanos a los límites definidos.

## Cobertura

Ejecutar las pruebas con cobertura:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Ejecutar con un umbral mínimo del 80 %:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Generar un reporte HTML:

```bash
poetry run pytest --cov=src --cov-report=html
```

El reporte se genera en:

```text
htmlcov/
```

La cobertura indica qué parte del código fue ejecutada por las pruebas, pero no garantiza por sí sola que todas las pruebas estén bien diseñadas.

## Integración continua

El workflow se encuentra en:

```text
.github/workflows/tests.yml
```

CI ejecuta:

- Instalación de Python 3.12.
- Instalación de Poetry.
- Instalación de dependencias.
- Suite de pruebas.
- Reporte y umbral de cobertura.
- mypy.
- Ruff.
- Comprobación de Black.

El flujo se activa con:

- `push`.
- `pull_request`.

## Validación de calidad

Se utilizaron las herramientas configuradas previamente:

```bash
poetry run ruff check src
```

```bash
poetry run black --check src
```

```bash
poetry run mypy src tests
```

```bash
poetry run pre-commit run --all-files
```

El hook de mypy requiere dependencias adicionales para analizar las pruebas:

```yaml
additional_dependencies:
  - pytest
  - hypothesis
```

## Archivos excluidos de Git

El archivo `.gitignore` excluye:

```text
.venv/
__pycache__/
*.py[cod]
.ruff_cache/
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/
```

## Comandos principales

Ejecutar todas las pruebas:

```bash
poetry run pytest -q
```

Ejecutar con información detallada:

```bash
poetry run pytest -v
```

Ejecutar una prueba específica:

```bash
poetry run pytest tests/test_ventas.py::test_generar_resumen_sin_ventas
```

Ejecutar pruebas unitarias:

```bash
poetry run pytest -m unit -q
```

Ejecutar cobertura:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

Ejecutar mypy:

```bash
poetry run mypy src tests
```

## Resultado del laboratorio

Se implementó una historia de ventas mediante TDD y se incorporaron:

- Pruebas unitarias.
- Ciclo Red–Green–Refactor.
- Fixtures reutilizables.
- Parametrización.
- Markers.
- Mocking con `unittest.mock`.
- Simulación de excepciones.
- Property-based testing con Hypothesis.
- Reporte de cobertura.
- Umbral mínimo de cobertura.
- Integración de pruebas en CI.
- Validación con Ruff, Black y mypy.


## Tablas de Problemas presentados

| Problema | Solución |
|---|---|
| Pytest no encontraba el paquete `src`. | Se creó `src/__init__.py` y se configuró `pythonpath = ["."]` en `pyproject.toml`. |
| La función `generar_resumen` no existía. | Se implementó el código mínimo para pasar la primera prueba del ciclo TDD. |
| La implementación inicial no procesaba ventas reales. | Se agregó el cálculo de la cantidad de ventas y del ingreso total. |
| No se validaban cantidades ni precios inválidos. | Se añadieron validaciones que lanzan `ValueError`. |
| Mypy no encontraba `pytest` ni `hypothesis`. | Se agregaron como dependencias adicionales del hook de mypy. |
| Faltaban anotaciones en fixtures y funciones de prueba. | Se añadieron tipos de retorno y tipos para los parámetros. |
| Los datos de prueba se inferían como `list[dict[str, object]]`. | Se anotaron explícitamente como `list[Venta]`. |
| La cobertura debía cumplir un umbral mínimo. | Se configuró `pytest-cov`, un reporte detallado y un umbral del 80 %. |
| La calidad debía comprobarse automáticamente. | Se configuraron Black, Ruff, mypy y pre-commit. |
| Las validaciones debían ejecutarse también en CI. | Se creó un workflow para pruebas, cobertura, mypy, Ruff y Black. |