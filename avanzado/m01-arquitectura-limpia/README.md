# Módulo Avanzado 01: Arquitectura Limpia

## Descripción

Este módulo implementa una estructura basada en Arquitectura Limpia para separar entidades, casos de uso, controladores, presenters y detalles de infraestructura.

El laboratorio introduce:

- Entidad `Order`.
- Caso de uso `CreateOrder`.
- DTOs.
- Unit of Work.
- Eventos de dominio.
- Presenter.
- Gateway de persistencia.
- Pruebas por capas.

## Objetivos

- Separar reglas de negocio de detalles técnicos.
- Definir límites claros entre capas.
- Coordinar transacciones mediante Unit of Work.
- Publicar eventos después de confirmar operaciones.
- Mantener los casos de uso independientes de frameworks e infraestructura.
- Probar entidades, casos de uso y eventos de forma aislada.

## Estructura del módulo

```text
m01-arquitectura-limpia/
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── dto.py
│   │   ├── handlers.py
│   │   ├── ports.py
│   │   ├── presenters.py
│   │   └── use_cases.py
│   ├── composition.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── orders.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities.py
│   │   └── events.py
│   └── infrastructure/
│       ├── __init__.py
│       ├── memory_notifier.py
│       ├── memory_uow.py
│       └── sqlalchemy_uow.py
└── tests/
    ├── test_domain.py
    ├── test_use_cases.py
    └── test_events.py
```

## Capas

La dirección general de dependencias es:

```text
Infraestructura → Aplicación → Dominio
```

### Dominio

Contiene:

- Entidades.
- Reglas de negocio.
- Eventos de dominio.
- Validaciones esenciales.

No depende de SQLAlchemy, FastAPI ni clientes externos.

### Aplicación

Contiene:

- Casos de uso.
- DTOs.
- Puertos.
- Presenters.
- Manejadores de eventos.
- Coordinación transaccional.

### Controladores

Adaptan las entradas externas al formato que necesita la aplicación.

### Infraestructura

Contiene:

- Unit of Work en memoria.
- Unit of Work con SQLAlchemy.
- Adaptadores de persistencia.
- Adaptadores de notificación.
- Detalles técnicos de almacenamiento.

## Entidad `Order`

La entidad se encuentra en:

```text
src/domain/entities.py
```

Se implementó como una dataclass inmutable:

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

La entidad valida:

- Producto no vacío.
- Cantidad mayor que cero.
- Precio unitario mayor que cero.

También calcula el total:

```python
@property
def total(self) -> float:
    return self.quantity * self.unit_price
```

## Evento `OrderCreated`

El evento se encuentra en:

```text
src/domain/events.py
```

```python
@dataclass(frozen=True)
class OrderCreated:
    order_id: int
    product: str
    total: float
```

Representa un hecho ocurrido:

```text
La orden fue creada.
```

El evento se acumula durante la operación y se publica después de confirmar el commit.

## DTOs

Los DTOs se encuentran en:

```text
src/application/dto.py
```

### `CreateOrderRequest`

Transporta los datos necesarios para crear una orden:

- `order_id`.
- `product`.
- `quantity`.
- `unit_price`.

### `OrderResponse`

Transporta la salida del caso de uso:

- `order_id`.
- `product`.
- `quantity`.
- `unit_price`.
- `total`.

El flujo es:

```text
CreateOrderRequest
        ↓
Order
        ↓
OrderResponse
```

## Puertos

Los puertos se encuentran en:

```text
src/application/ports.py
```

### `OrderRepository`

Define las operaciones de persistencia:

```python
class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        ...

    def get(self, order_id: int) -> Order | None:
        ...
```

### `UnitOfWork`

Coordina repositorios, eventos, commit y rollback:

```python
class UnitOfWork(Protocol):
    orders: OrderRepository
    events: list[OrderCreated]

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
```

### `EventPublisher`

Define la publicación de eventos:

```python
class EventPublisher(Protocol):
    def publish(self, event: OrderCreated) -> None:
        ...
```

## Caso de uso `CreateOrder`

El caso de uso se encuentra en:

```text
src/application/use_cases.py
```

Su flujo es:

```text
Recibir DTO
    ↓
Crear entidad
    ↓
Guardar mediante Unit of Work
    ↓
Acumular OrderCreated
    ↓
Confirmar commit
    ↓
Publicar evento
    ↓
Crear DTO de salida
```

Si ocurre una excepción:

```python
self._unit_of_work.rollback()
```

La publicación del evento ocurre después del commit para evitar notificar una operación que haya fallado.

## Unit of Work

### Implementación en memoria

Archivo:

```text
src/infrastructure/memory_uow.py
```

Se utiliza para:

- Pruebas rápidas.
- Pruebas aisladas.
- Simular commit.
- Simular rollback.
- Evitar infraestructura externa.

### Implementación SQLAlchemy

Archivo:

```text
src/infrastructure/sqlalchemy_uow.py
```

Utiliza:

- SQLite en memoria.
- SQLAlchemy.
- Un repositorio SQL.
- Una sesión.
- Commit y rollback reales.

## Controller y Presenter

### Controller

Archivo:

```text
src/controllers/orders.py
```

`OrderController`:

- Recibe datos de entrada.
- Construye `CreateOrderRequest`.
- Ejecuta `CreateOrder`.
- Envía el resultado al Presenter.

### Presenter

Archivo:

```text
src/application/presenters.py
```

`OrderPresenter` transforma `OrderResponse` en un diccionario de salida:

```python
{
    "id": response.order_id,
    "product": response.product,
    "quantity": response.quantity,
    "unit_price": response.unit_price,
    "total": response.total,
}
```

## Wiring y composición

El archivo:

```text
src/composition.py
```

conecta:

```text
UnitOfWork
    ↓
EventPublisher
    ↓
CreateOrder
    ↓
OrderController
    ↓
OrderPresenter
```

El wiring selecciona las implementaciones concretas, mientras el caso de uso depende de los puertos.

## Eventos y manejadores

Los eventos se publican después del commit.

El flujo es:

```text
Guardar cambios
    ↓
Acumular evento
    ↓
Commit exitoso
    ↓
Publicar OrderCreated
    ↓
Ejecutar manejador
```

Si el commit falla:

- Se ejecuta rollback.
- El evento no se publica.
- La excepción se propaga.

## Pruebas

Las pruebas cubren:

- Cálculo del total.
- Validaciones de la entidad.
- Creación de órdenes.
- Commit.
- Rollback.
- Publicación de eventos.
- Uso del Presenter.
- Wiring con implementaciones en memoria.
- Persistencia mediante SQLAlchemy.

Ejecutar las pruebas:

```bash
poetry run pytest tests -q
```

Resultado esperado:

```text
7 passed
```

## Validación de calidad

Ejecutar mypy:

```bash
poetry run mypy src tests
```

Ejecutar Ruff:

```bash
poetry run ruff check src tests
```

Aplicar formato con Black:

```bash
poetry run black src tests
```

Comprobar formato:

```bash
poetry run black --check src tests
```

## Excepción localizada de SQLAlchemy

El módulo utiliza SQLAlchemy `1.4.54` debido a una restricción corporativa que bloqueó extensiones compiladas de versiones más recientes.

Además, los stubs utilizados no reconocen completamente algunos elementos dinámicos de SQLAlchemy 1.4, como `declarative_base`.

Por ello se mantienen excepciones localizadas:

```python
from sqlalchemy.orm import declarative_base  # type: ignore[attr-defined]
```

y, cuando es necesario:

```python
class OrderModel(Base):  # type: ignore[misc, valid-type]
```

Ruff no reorganiza los imports de ese archivo para conservar la excepción en la línea correcta.

Estas excepciones:

- Se limitan al adaptador SQLAlchemy.
- No desactivan mypy globalmente.
- Documentan una incompatibilidad concreta entre SQLAlchemy 1.4.54 y sus stubs.

## Resultado del módulo

Se implementó una estructura de Arquitectura Limpia con:

- Entidad de dominio `Order`.
- Caso de uso `CreateOrder`.
- DTOs de entrada y salida.
- Unit of Work.
- Commit y rollback.
- Evento `OrderCreated`.
- Presenter.
- Controller.
- Wiring de dependencias.
- Pruebas de dominio y aplicación.
- Adaptador SQLAlchemy.
- Implementación en memoria.