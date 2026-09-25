# Módulo 05: Principios SOLID aplicados en Python

## Descripción

Este módulo aplica los principios SOLID al diseño de servicios y componentes Python.

El laboratorio refactoriza un servicio de órdenes para que dependa de un puerto definido mediante `Protocol`. Se implementan dos repositorios sustituibles:

- Repositorio en memoria.
- Repositorio SQL mediante `sqlite3`.

## Objetivos

- Aplicar SOLID a servicios y dominio.
- Reducir el acoplamiento.
- Mejorar la cohesión.
- Facilitar la extensibilidad.
- Diseñar dependencias sustituibles.
- Verificar el principio de sustitución de Liskov.
- Mejorar la testabilidad.

## Estructura del módulo

```text
m05-solid/
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── domain.py
│   ├── main.py
│   ├── ports.py
│   ├── providers.py
│   ├── repositories.py
│   └── services.py
└── tests/
    └── test_services.py
```

## Entidad de dominio

La entidad se encuentra en:

```text
src/domain.py
```

Se definió `Order` como una dataclass inmutable:

```python
@dataclass(frozen=True)
class Order:
    ...
```

Sus atributos son:

- `order_id`.
- `product`.
- `quantity`.
- `unit_price`.

También expone una propiedad calculada:

```python
@property
def total(self) -> float:
    ...
```

El total se calcula como:

```text
quantity × unit_price
```

## Puerto `OrderRepository`

El contrato se define en:

```text
src/ports.py
```

```python
class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        ...

    def get(self, order_id: int) -> Order | None:
        ...
```

El puerto especifica las operaciones necesarias, pero no define cómo se almacenan las órdenes.

Las implementaciones compatibles deben:

- Guardar una orden.
- Recuperar una orden por identificador.
- Devolver `None` si no existe.

## Implementación en memoria

La clase:

```python
InMemoryOrderRepository
```

utiliza un diccionario interno:

```python
dict[int, Order]
```

Características:

- No requiere una base de datos.
- Es rápida.
- Es útil para pruebas.
- Los datos desaparecen al finalizar el proceso.

## Implementación SQL

La clase:

```python
SqlOrderRepository
```

utiliza `sqlite3`.

Características:

- Crea una tabla `orders`.
- Guarda órdenes mediante SQL parametrizado.
- Recupera órdenes por identificador.
- Utiliza una conexión proporcionada externamente.
- Cumple el mismo contrato que el repositorio en memoria.

## Servicio desacoplado

El servicio se encuentra en:

```text
src/services.py
```

```python
class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository
```

El servicio depende del protocolo `OrderRepository`, no de una implementación concreta.

### Responsabilidades del servicio

- Validar cantidades.
- Validar precios.
- Guardar órdenes.
- Recuperar órdenes.
- Coordinar la lógica de aplicación.

### Validaciones

Se rechazan:

- Cantidades menores o iguales que cero.
- Precios menores o iguales que cero.

Los valores inválidos producen:

```python
ValueError
```

## Factory y providers

La creación de repositorios se encuentra en:

```text
src/providers.py
```

### Providers

Los providers crean implementaciones listas para utilizar:

```python
provide_memory_repository()
provide_sql_repository(connection)
```

### Factory

La factory selecciona la implementación según un tipo:

```python
create_repository("memory")
create_repository("sql", connection)
```

Esto permite cambiar el almacenamiento sin modificar `OrderService`.

## Aplicación de SOLID

### SRP

Cada componente tiene una responsabilidad principal:

- `Order`: representa la entidad.
- `OrderService`: contiene lógica de aplicación.
- `InMemoryOrderRepository`: almacena en memoria.
- `SqlOrderRepository`: almacena mediante SQL.
- `providers.py`: crea implementaciones.

### OCP

Se puede agregar un nuevo repositorio sin modificar el servicio:

```python
class ApiOrderRepository:
    ...
```

Mientras cumpla `OrderRepository`, puede incorporarse mediante una nueva configuración o factory.

### LSP

`InMemoryOrderRepository` y `SqlOrderRepository` pueden sustituirse detrás del mismo protocolo.

El servicio funciona con ambas implementaciones sin cambiar su código.

### ISP

El puerto define únicamente las operaciones que el servicio necesita:

- `save`.
- `get`.

No obliga a las implementaciones a incluir métodos innecesarios.

### DIP

`OrderService` depende de la abstracción:

```python
OrderRepository
```

y no de detalles concretos como:

```python
InMemoryOrderRepository
SqlOrderRepository
```

## Flujo de dependencias

```text
OrderService
      ↓
OrderRepository (Protocol)
      ↓
┌─────────────────────────┐
│ InMemoryOrderRepository │
│ SqlOrderRepository      │
└─────────────────────────┘
```

## Ejecución

Desde la raíz del módulo:

```bash
poetry run python -m src.main
```

La ejecución utiliza ambas implementaciones y muestra los resultados recuperados.

La salida esperada contiene órdenes equivalentes:

```text
Order(order_id=1, product='Teclado', quantity=2, unit_price=50.0)
Order(order_id=1, product='Teclado', quantity=2, unit_price=50.0)
True
```

El último valor confirma que ambas entidades son equivalentes.

## Pruebas

Las pruebas se encuentran en:

```text
tests/test_services.py
```

Se verifica:

- Funcionamiento con el repositorio en memoria.
- Funcionamiento con el repositorio SQL.
- Equivalencia de resultados.
- Validación de cantidades inválidas.
- Validación de precios inválidos.
- Sustitución de implementaciones mediante el mismo puerto.

Ejecutar las pruebas:

```bash
poetry run pytest tests -q
```

## Prueba parametrizada

La prueba principal utiliza parametrización para ejecutar el mismo comportamiento con ambos repositorios:

```python
@pytest.mark.parametrize("kind", ["memory", "sql"])
```

Esto comprueba que el servicio no dependa de una implementación específica.

## Verificación de tipos y calidad

Las herramientas de calidad se ejecutan según la configuración del repositorio consolidado.

Comprobar tipos localmente:

```bash
poetry run mypy src tests
```

Analizar calidad:

```bash
poetry run ruff check src tests
```

Comprobar formato:

```bash
poetry run black --check src tests
```

Ejecutar hooks desde la raíz del repositorio:

```bash
pre-commit run --all-files
```

## Resultado del módulo

Se implementó un servicio de órdenes desacoplado mediante un puerto `Protocol`.

El mismo servicio funciona con:

- Un repositorio en memoria.
- Un repositorio SQL.

La solución aplica:

- Separación de responsabilidades.
- Inversión de dependencias.
- Inyección de dependencias.
- Factory y providers.
- Sustitución de implementaciones.
- Verificación práctica de LSP.
- Mejora de la testabilidad.