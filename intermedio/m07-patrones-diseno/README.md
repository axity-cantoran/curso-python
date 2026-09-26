# Módulo 07: Patrones de diseño

## Descripción

Este módulo implementa patrones de diseño aplicados a un sistema de cálculo de precios.

El laboratorio utiliza:

- Strategy para seleccionar políticas de precios.
- Decorator para almacenar resultados en caché.
- Adapter para integrar un proveedor externo.
- Pruebas con pytest y mocks.

## Objetivos

- Implementar patrones relevantes con ejemplos reales.
- Seleccionar patrones según el problema.
- Identificar señales de refactorización.
- Reconocer antipatrones.
- Reducir acoplamiento.
- Facilitar la extensión y las pruebas.

## Estructura del módulo

```text
m07-patrones-diseno/
├── README.md
├── poetry.lock
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── adapters.py
│   ├── cache.py
│   ├── main.py
│   └── pricing.py
└── tests/
    └── test_patterns.py
```

## Strategy para precios

El patrón Strategy permite encapsular algoritmos intercambiables detrás de una interfaz común.

El contrato se define mediante:

```python
class PricingStrategy(Protocol):
    def calculate(self, price: float) -> float:
        ...
```

Se implementaron tres estrategias:

- `RegularPricing`: conserva el precio original.
- `DiscountPricing`: aplica un descuento configurable.
- `PremiumPricing`: aplica una reducción para clientes premium.

El contexto es:

```python
class PriceCalculator:
    ...
```

El contexto recibe una estrategia y delega el cálculo:

```python
calculator = PriceCalculator(
    DiscountPricing(0.10)
)
```

Resultado:

```text
Precio base: 100.0
Precio final: 90.0
```

### Ventajas de Strategy

- Evita cadenas extensas de `if`.
- Permite intercambiar algoritmos.
- Facilita probar cada estrategia.
- Permite agregar nuevas políticas sin modificar el contexto.
- Aplica el principio Open/Closed.

## Decorator de caché

El archivo `src/cache.py` contiene el decorador:

```python
def cached(...):
    ...
```

El decorador:

- Recibe una función.
- Guarda los resultados.
- Utiliza los argumentos como clave.
- Devuelve el resultado almacenado en llamadas repetidas.
- Conserva los metadatos mediante `functools.wraps`.

Ejemplo conceptual:

```python
@cached
def calcular(precio: float) -> float:
    return precio * 2
```

Primera llamada:

```python
calcular(10)
```

Ejecuta la función.

Segunda llamada:

```python
calcular(10)
```

Devuelve el valor almacenado sin repetir el cálculo.

### Consideraciones

La clave de caché se construye a partir de los argumentos. Por eso, los argumentos deben ser compatibles con la construcción de una clave hashable.

El decorador es adecuado para funciones cuyo resultado depende de sus argumentos y que no producen efectos secundarios importantes.

## Adapter para proveedor externo

El archivo `src/adapters.py` contiene un proveedor externo con una interfaz diferente:

```python
class ExternalPriceService:
    def fetch_current_price(
        self,
        external_code: str,
    ) -> dict[str, object]:
        ...
```

La aplicación espera:

```python
class PriceProvider(Protocol):
    def get_price(self, product_id: str) -> float:
        ...
```

El adaptador traduce ambas interfaces:

```python
class ExternalPriceAdapter:
    ...
```

La conversión es:

```text
get_price(product_id)
        ↓
fetch_current_price(external_code)
        ↓
response["amount"]
```

### Ventajas de Adapter

- Evita modificar el proveedor externo.
- Aísla diferencias de nombres y formatos.
- Permite utilizar servicios incompatibles.
- Mantiene estable la interfaz esperada por la aplicación.
- Facilita sustituir el proveedor durante las pruebas.

## Integración de los patrones

El flujo principal es:

```text
Proveedor externo
        ↓
Adapter
        ↓
PriceProvider
        ↓
Decorator de caché
        ↓
Strategy de precios
        ↓
Precio final
```

El archivo `src/main.py` integra los componentes:

```python
provider = ExternalPriceAdapter(
    ExternalPriceService()
)

precio = obtener_precio(provider, "SKU-001")

calculator = PriceCalculator(
    DiscountPricing(0.10)
)

precio_final = calculator.calculate(precio)
```

## Pruebas

Las pruebas se encuentran en:

```text
tests/test_patterns.py
```

Se probaron:

- Estrategia de precio regular.
- Estrategia de descuento.
- Estrategia premium.
- Rechazo de precios negativos.
- Caché de resultados.
- Evitar ejecuciones repetidas.
- Adaptación de respuestas externas.
- Rechazo de precios no numéricos.
- Verificación de llamadas al proveedor.

Ejecutar las pruebas:

```bash
poetry run pytest tests -q
```

Resultado esperado:

```text
7 passed
```

## Parametrización

Las estrategias se prueban mediante parametrización:

```python
@pytest.mark.parametrize(
    ("strategy", "expected"),
    [
        (RegularPricing(), 100.0),
        (DiscountPricing(0.10), 90.0),
        (PremiumPricing(), 85.0),
    ],
)
```

Esto permite comprobar varios comportamientos con una misma prueba.

## Mocking

El proveedor externo se sustituye mediante un mock:

```python
service = Mock()
service.fetch_current_price.return_value = {
    "code": "SKU-001",
    "amount": 100.0,
}
```

También se verifican las llamadas:

```python
service.fetch_current_price.assert_called_once_with(
    "SKU-001"
)
```

Esto evita depender de un servicio real durante las pruebas.

## Patrones aplicados

| Patrón | Uso en el módulo |
|---|---|
| Strategy | Seleccionar políticas de precios |
| Decorator | Agregar caché sin modificar la función |
| Adapter | Traducir la interfaz del proveedor externo |
| Protocol | Definir contratos estructurales |

## Señales de refactorización

En este módulo se identificaron como señales:

- Cadenas extensas de `if`.
- Varias reglas de cálculo dentro de una misma función.
- Dependencia directa de un proveedor externo.
- Necesidad de añadir caché sin modificar una función estable.
- Dificultad para probar cada comportamiento por separado.

## Antipatrones evitados

- Condicionales crecientes para cada política de precio.
- Acoplamiento directo con el proveedor externo.
- Modificación de una función estable para agregar caché.
- Dependencia de servicios reales durante las pruebas.
- Abstracciones innecesarias para problemas simples.

## Ejecución

Desde la raíz del módulo:

```bash
poetry run python -m src.main
```

Salida esperada:

```text
Precio base: 100.0
Precio final: 90.0
```

## Validación de calidad

Ejecutar Ruff:

```bash
poetry run ruff check src tests
```

Formatear con Black:

```bash
poetry run black src tests
```

Comprobar formato:

```bash
poetry run black --check src tests
```

Ejecutar mypy:

```bash
poetry run mypy src tests
```

Los hooks del repositorio consolidado se ejecutan desde la raíz de `curso-python`:

```bash
pre-commit run --all-files
```

## Resultado del módulo

Se implementó un sistema de cálculo de precios que utiliza Strategy, Decorator y Adapter.

La solución permite:

- Cambiar políticas de precio.
- Reutilizar resultados mediante caché.
- Integrar un proveedor externo incompatible.
- Probar cada componente de forma aislada.
- Mantener bajo acoplamiento.
- Extender comportamientos sin modificar código estable.