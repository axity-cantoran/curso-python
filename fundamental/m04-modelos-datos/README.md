# Módulo 04: Objetos y modelos de datos

## Descripción

Este módulo muestra cómo modelar entidades con clases y dataclasses, validar datos externos con Pydantic y convertir información entre modelos de entrada, entidades internas y modelos de salida.

El laboratorio implementa una entidad `Order` con cálculos derivados y comparaciones, además de los modelos Pydantic `OrderIn` y `OrderOut`.

## Objetivos

- Modelar entidades con atributos y comportamiento.
- Utilizar `dataclass` para reducir código repetitivo.
- Implementar cálculos derivados.
- Definir comparaciones mediante métodos especiales.
- Validar entradas con Pydantic.
- Serializar modelos a diccionarios y JSON.
- Separar modelos externos de la entidad interna.

## Entorno

- Python 3.12
- Poetry
- Ambiente virtual `.venv`
- Visual Studio Code
- Git Bash
- Pydantic
- Black
- isort
- Ruff
- pre-commit
- Git local

## Configuración del proyecto

El proyecto utiliza Poetry para gestionar el ambiente virtual y las dependencias.

El ambiente virtual se crea dentro del proyecto:

```text
.venv/
```

El proyecto se configuró con:

```toml
[tool.poetry]
package-mode = false
```

Esto indica que Poetry se utiliza como gestor de dependencias y herramientas, sin instalar el proyecto como un paquete Python.

## Estructura del proyecto

```text
m04-modelos-datos/
├── .git/
├── .gitignore
├── .pre-commit-config.yaml
├── .venv/
├── poetry.lock
├── pyproject.toml
├── README.md
└── src/
    ├── entidades.py
    ├── main.py
    └── modelos.py
```

### Archivos principales

- `src/entidades.py`: contiene la entidad `Order`.
- `src/modelos.py`: contiene los modelos Pydantic `OrderIn` y `OrderOut`.
- `src/main.py`: coordina la validación, conversión, comparación y serialización.
- `pyproject.toml`: contiene la configuración del proyecto y sus herramientas.
- `.pre-commit-config.yaml`: define los hooks automáticos.
- `.gitignore`: excluye archivos y carpetas locales.

## Entidad `Order`

La entidad se implementó como una `dataclass`:

```python
@dataclass
class Order:
    ...
```

Sus atributos principales son:

- `order_id`
- `product`
- `unit_price`
- `quantity`
- `tax_rate`

También contiene atributos calculados:

- `subtotal`
- `tax`
- `total`

## Cálculos derivados

Los valores calculados se generan en `__post_init__`:

```python
def __post_init__(self):
    ...
```

Las fórmulas utilizadas son:

```text
subtotal = unit_price × quantity
tax = subtotal × tax_rate
total = subtotal + tax
```

Por ejemplo, para:

```text
unit_price = 50
quantity = 2
tax_rate = 0.16
```

el resultado es:

```text
subtotal = 100.00
tax = 16.00
total = 116.00
```

Los campos derivados utilizan:

```python
field(init=False)
```

Por ello, no se reciben como argumentos al crear la entidad.

## Métodos especiales

La entidad `Order` implementa:

### `__str__`

Proporciona una representación legible:

```text
Order ORD-001: Teclado - Total: 116.00
```

### `__eq__`

Define la igualdad entre órdenes utilizando `order_id`.

Dos órdenes con el mismo identificador se consideran iguales aunque tengan otros datos diferentes.

### `__lt__`

Permite utilizar el operador `<` para comparar órdenes según su `total`.

Ejemplo:

```python
order_a < order_b
```

devuelve `True` si el total de `order_a` es menor.

## Modelo `OrderIn`

`OrderIn` representa los datos de entrada y utiliza Pydantic para validarlos:

```python
class OrderIn(BaseModel):
    ...
```

### Validaciones

- `order_id` no puede estar vacío.
- `product` no puede estar vacío.
- `unit_price` debe ser mayor que cero.
- `quantity` debe ser mayor que cero.
- `tax_rate` debe estar entre `0` y `1`.

Ejemplo válido:

```python
OrderIn(
    order_id="ORD-001",
    product="Teclado",
    unit_price=50,
    quantity=2,
    tax_rate=0.16,
)
```

Pydantic puede convertir algunos valores compatibles, por ejemplo:

```python
unit_price="50"
```

a:

```python
unit_price=50.0
```

## Modelo `OrderOut`

`OrderOut` representa los datos de salida:

```python
class OrderOut(BaseModel):
    ...
    ```

Incluye los datos principales y los valores derivados:

- `order_id`
- `product`
- `unit_price`
- `quantity`
- `tax_rate`
- `subtotal`
- `tax`
- `total`

## Flujo de conversión

El flujo principal del laboratorio es:

```text
Datos externos
    ↓
OrderIn
    ↓ validación
Order
    ↓ cálculos derivados
OrderOut
    ↓ serialización
Diccionario o JSON
```

### Conversión de `OrderIn` a `Order`

La función:

```python
def order_in_to_entity(order_in: OrderIn) -> Order:
    ...
```

recibe un modelo validado y crea la entidad interna.

### Conversión de `Order` a `OrderOut`

La función:

```python
def order_to_order_out(order: Order) -> OrderOut:
    ...
```

crea el modelo de salida utilizando los atributos originales y los cálculos derivados.

## Serialización

Para convertir `OrderOut` en un diccionario Python:

```python
order_out.model_dump()
```

Para convertirlo en JSON:

```python
order_out.model_dump_json()
```

### Diccionario Python

```python
{
    'order_id': 'ORD-001',
    'product': 'Teclado',
    'total': 116.0
}
```

### JSON

```json
{"order_id":"ORD-001","product":"Teclado","total":116.0}
```

`model_dump()` devuelve un `dict` de Python. `model_dump_json()` devuelve una cadena de texto con formato JSON.

## Manejo de validaciones

Los datos inválidos generan `ValidationError`.

Ejemplo:

```python
try:
    order_in = OrderIn(...)
except ValidationError as error:
    print(f"Datos inválidos:\n{error}")
```

Se probaron casos como:

- Identificador vacío.
- Producto vacío.
- Precio negativo.
- Cantidad igual a cero.
- Porcentaje de impuesto superior a `1`.

La validación ocurre antes de crear la entidad `Order`.

## Ejecución

Desde la raíz del proyecto:

```bash
poetry run python src/main.py
```

La salida esperada incluye:

```text
Order ORD-001: Teclado - Total: 116.00
```

También se muestran:

- Comparaciones entre órdenes.
- Diccionario generado con `model_dump()`.
- JSON generado con `model_dump_json()`.

## Validación del código

- A partir de aquí, son las mismas anotaciones sobre lo realizado en el módulo 01 - Entorno y Herramientas.
- Dada la misma configuración, no se repetirá.
