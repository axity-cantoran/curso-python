# Módulo 06: Arquitectura Hexagonal

## Descripción

Este módulo implementa una arquitectura hexagonal basada en puertos y adaptadores.

La solución separa:

- Dominio.
- Aplicación.
- Infraestructura.

El laboratorio implementa el caso de uso `CreateOrder` con repositorios intercambiables y un adaptador de notificación HTTP simulado.

## Objetivos

- Separar reglas de negocio de detalles técnicos.
- Definir puertos estables mediante `Protocol`.
- Implementar adaptadores intercambiables.
- Aplicar inyección de dependencias.
- Separar entidades y DTOs.
- Probar reglas de dominio y contratos de adaptadores.
- Facilitar la sustitución de infraestructura.

## Estructura del módulo

```text
m06-arquitectura-hexagonal/
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── entities.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── dto.py
│   │   ├── ports.py
│   │   └── use_cases.py
│   └── infrastructure/
│       ├── __init__.py
│       ├── http_notifier.py
│       ├── memory_notifier.py
│       ├── memory_repository.py
│       └── sqlalchemy_repository.py
└── tests/
    ├── test_create_order.py
    └── test_sqlalchemy_repository.py
```

## Capas

### Dominio

Se encuentra en:

```text
src/domain/
```

Contiene:

- Entidades.
- Reglas de negocio.
- Cálculos propios del dominio.
- Validaciones independientes de infraestructura.

El dominio no depende de SQLAlchemy, HTTP ni frameworks.

### Aplicación

Se encuentra en:

```text
src/application/
```

Contiene:

- Casos de uso.
- DTOs.
- Puertos.
- Orquestación de operaciones.

La aplicación coordina el flujo y utiliza puertos en lugar de depender de adaptadores concretos.

### Infraestructura

Se encuentra en:

```text
src/infrastructure/
```

Contiene:

- Persistencia en memoria.
- Persistencia SQLAlchemy.
- Notificaciones HTTP.
- Implementaciones concretas de los puertos.

## Entidad `Order`

La entidad se encuentra en:

```text
src/domain/entities.py
```

Se definió como una `dataclass` inmutable:

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

- Cantidad mayor que cero.
- Precio unitario mayor que cero.

También calcula el total:

```python
@property
def total(self) -> float:
    return self.quantity * self.unit_price
```

## DTOs

Los DTOs se encuentran en:

```text
src/application/dto.py
```

### `CreateOrderRequest`

Transporta los datos necesarios para solicitar la creación de una orden:

- `product`.
- `quantity`.
- `unit_price`.

### `OrderResponse`

Transporta el resultado del caso de uso:

- `order_id`.
- `product`.
- `quantity`.
- `unit_price`.
- `total`.

El flujo de conversión es:

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

### `OrderNotifier`

Define la operación de notificación:

```python
class OrderNotifier(Protocol):
    def notify_order_created(self, order: Order) -> None:
        ...
```

Los puertos definen contratos, no detalles de implementación.

## Caso de uso `CreateOrder`

El caso de uso se encuentra en:

```text
src/application/use_cases.py
```

`CreateOrder` recibe sus dependencias mediante el constructor:

```python
class CreateOrder:
    def __init__(
        self,
        repository: OrderRepository,
        notifier: OrderNotifier,
    ) -> None:
        self._repository = repository
        self._notifier = notifier
```

Su flujo es:

```text
Recibir DTO de entrada
        ↓
Crear entidad Order
        ↓
Guardar mediante OrderRepository
        ↓
Notificar mediante OrderNotifier
        ↓
Crear DTO de salida
```

El caso de uso no conoce:

- SQLite.
- SQLAlchemy.
- HTTP.
- FastAPI.
- La implementación concreta de los adaptadores.

## Adaptador en memoria

Archivos:

```text
src/infrastructure/memory_repository.py
src/infrastructure/memory_notifier.py
```

El repositorio en memoria utiliza un diccionario para almacenar órdenes.

Ventajas:

- No requiere infraestructura externa.
- Es rápido.
- Es útil para pruebas.
- Permite verificar el comportamiento del caso de uso.

El notificador en memoria almacena las notificaciones generadas para poder verificarlas durante las pruebas.

## Adaptador SQLAlchemy

Archivo:

```text
src/infrastructure/sqlalchemy_repository.py
```

El adaptador SQLAlchemy:

- Utiliza SQLite en memoria.
- Define un modelo persistente.
- Crea la tabla `orders`.
- Guarda entidades `Order`.
- Recupera entidades por identificador.
- Convierte entre el modelo SQL y la entidad de dominio.

El caso de uso no necesita conocer estos detalles.

## Adaptador HTTP

Archivo:

```text
src/infrastructure/http_notifier.py
```

El adaptador HTTP implementa `OrderNotifier` y envía una solicitud a un servicio externo:

```python
class HttpOrderNotifier:
    ...
```

La aplicación solo conoce:

```python
OrderNotifier
```

No conoce los detalles de `httpx`, URL, encabezados ni formato HTTP.

## Inyección de dependencias

Las dependencias se proporcionan desde fuera:

```python
repository = InMemoryOrderRepository()
notifier = InMemoryOrderNotifier()

use_case = CreateOrder(
    repository=repository,
    notifier=notifier,
)
```

Esto permite cambiar los adaptadores sin modificar `CreateOrder`.

Ejemplo con SQLAlchemy:

```python
repository = SqlAlchemyOrderRepository()
notifier = InMemoryOrderNotifier()

use_case = CreateOrder(repository, notifier)
```

## Principios aplicados

### Separación de responsabilidades

Cada componente tiene un propósito definido:

- `Order`: reglas del dominio.
- `CreateOrder`: orquestación.
- `OrderRepository`: contrato de persistencia.
- `OrderNotifier`: contrato de notificación.
- Repositorios: almacenamiento.
- Notificadores: comunicación externa.

### Inversión de dependencias

La aplicación depende de puertos:

```text
Caso de uso → Protocol
```

Los adaptadores implementan esos puertos:

```text
Adaptador → Protocol
```

La relación conceptual es:

```text
Aplicación → Puerto ← Adaptador
```

### Sustitución de implementaciones

El mismo caso de uso funciona con:

- `InMemoryOrderRepository`.
- `SqlAlchemyOrderRepository`.

La implementación puede cambiar sin modificar la lógica de aplicación.

## Pruebas

Las pruebas se encuentran en:

```text
tests/
```

### Pruebas de dominio

Verifican:

- Creación de entidades.
- Validación de cantidad.
- Validación de precio.
- Cálculo del total.

### Pruebas del caso de uso

Verifican:

- Creación de una orden.
- Persistencia mediante el repositorio.
- Notificación de la orden.
- Generación del DTO de salida.

### Pruebas de contrato

Verifican que una implementación:

- Guarde una orden.
- Recupere la misma orden.
- Devuelva `None` para una orden inexistente.
- Respete el contrato del puerto.

El mismo comportamiento puede probarse con diferentes adaptadores.

### Pruebas del adaptador SQLAlchemy

Verifican:

- Creación de la tabla.
- Persistencia.
- Recuperación.
- Conversión entre modelo SQL y entidad.

## Ejecución

Desde la raíz del módulo:

```bash
poetry run pytest tests -q
```

Ejecutar el flujo del caso de uso:

```bash
poetry run python -c "from src.application.dto import CreateOrderRequest; from src.application.use_cases import CreateOrder; from src.infrastructure.memory_repository import InMemoryOrderRepository; from src.infrastructure.memory_notifier import InMemoryOrderNotifier; repository=InMemoryOrderRepository(); notifier=InMemoryOrderNotifier(); use_case=CreateOrder(repository, notifier); result=use_case.execute(CreateOrderRequest('Teclado', 2, 50.0)); print(result)"
```

## Validación de calidad

Las herramientas se ejecutan desde el ambiente del módulo:

```bash
poetry run mypy src tests
```

```bash
poetry run ruff check src tests
```

```bash
poetry run black --check src tests
```

Los hooks del repositorio consolidado se ejecutan desde la raíz de `curso-python`:

```bash
pre-commit run --all-files
```

## Excepción localizada de SQLAlchemy

El proyecto utiliza SQLAlchemy 1.4.54 debido a una restricción corporativa que bloqueó una extensión compilada de versiones más recientes.

Además, mypy y los stubs utilizados no reconocen completamente algunos elementos dinámicos de SQLAlchemy 1.4, como `declarative_base`.

Por ello se conservan excepciones localizadas, por ejemplo:

```python
from sqlalchemy.orm import declarative_base  # type: ignore[attr-defined]
```

Estas excepciones:

- Se limitan al adaptador SQLAlchemy.
- No desactivan globalmente el análisis de mypy.
- Documentan una incompatibilidad concreta entre la biblioteca y sus stubs.

## Resultado del módulo

Se implementó una arquitectura hexagonal con:

- Entidad de dominio `Order`.
- DTOs de entrada y salida.
- Caso de uso `CreateOrder`.
- Puerto de repositorio.
- Puerto de notificación.
- Adaptador en memoria.
- Adaptador SQLAlchemy.
- Adaptador HTTP simulado.
- Inyección de dependencias.
- Pruebas de dominio y contrato.
- Adaptadores intercambiables.