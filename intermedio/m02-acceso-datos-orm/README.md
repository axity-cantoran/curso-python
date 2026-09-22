# Módulo 02: Acceso a datos y ORM

## Descripción

Este módulo implementa el acceso a una base de datos relacional mediante SQLAlchemy y Alembic.

Se definieron modelos ORM para usuarios, órdenes y elementos de órdenes. También se implementaron operaciones CRUD, relaciones entre entidades, migraciones versionadas y pruebas aisladas con SQLite en memoria.

## Objetivos

- Modelar entidades y relaciones mediante SQLAlchemy ORM.
- Gestionar sesiones y transacciones.
- Implementar operaciones CRUD.
- Administrar cambios del esquema mediante Alembic.
- Probar el acceso a datos utilizando SQLite en memoria.
- Validar operaciones exitosas y errores de persistencia.

## Estructura del proyecto

```text
m02-acceso-datos-orm/
├── alembic.ini
├── migrations/
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── *_crea_tablas_iniciales.py
├── src/
│   ├── __init__.py
│   ├── base_datos.py
│   ├── main.py
│   ├── modelos.py
│   └── repositorio.py
├── tests/
│   ├── conftest.py
│   └── test_repositorio.py
├── app.db
├── pyproject.toml
└── README.md
```

El archivo `app.db` se utiliza como base de datos local de desarrollo y está excluido de Git.

## Modelos ORM

Los modelos se definieron en:

```text
src/modelos.py
```

La clase base declarativa es:

```python
class Base(DeclarativeBase):
    pass
```

### `User`

Representa a un usuario.

Campos principales:

- `id`
- `name`
- `email`
- `created_at`

El campo `email` es obligatorio y único.

### `Order`

Representa una orden perteneciente a un usuario.

Campos principales:

- `id`
- `user_id`
- `created_at`

### `OrderItem`

Representa un producto incluido en una orden.

Campos principales:

- `id`
- `order_id`
- `product`
- `quantity`
- `unit_price`

## Relaciones

La estructura de relaciones es:

```text
User 1 ─── * Order 1 ─── * OrderItem
```

Esto significa:

- Un usuario puede tener muchas órdenes.
- Una orden pertenece a un usuario.
- Una orden puede tener muchos elementos.
- Cada elemento pertenece a una orden.

### Claves foráneas

La relación entre usuarios y órdenes utiliza:

```text
orders.user_id → users.id
```

La relación entre órdenes y elementos utiliza:

```text
order_items.order_id → orders.id
```

### Relaciones ORM

Las relaciones se definieron mediante `relationship`:

```python
orders: Mapped[list[Order]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan",
)
```

```python
items: Mapped[list[OrderItem]] = relationship(
    back_populates="order",
    cascade="all, delete-orphan",
)
```

La configuración `cascade="all, delete-orphan"` permite propagar operaciones y eliminar elementos que quedan desvinculados de su entidad principal.

## Engine y sesiones

La configuración de la base de datos se encuentra en:

```text
src/base_datos.py
```

La conexión local utiliza SQLite:

```text
sqlite:///app.db
```

El `engine` administra la comunicación con la base de datos y las conexiones.

Las sesiones se crean mediante `SessionLocal`:

```python
with SessionLocal() as session:
    ...
```

La sesión administra:

- Entidades nuevas.
- Cambios.
- Eliminaciones.
- Consultas.
- Transacciones.

## Operaciones CRUD

El archivo:

```text
src/repositorio.py
```

contiene las operaciones de acceso a datos.

### Crear

Se implementaron funciones para crear:

- Usuarios.
- Órdenes.
- Elementos de órdenes.

Cada operación agrega la entidad a la sesión, confirma la transacción y actualiza el objeto generado.

### Consultar

Se implementaron funciones para:

- Obtener un usuario por su identificador.
- Obtener una orden por su identificador.
- Listar las órdenes de un usuario.

Ejemplo conceptual:

```python
consulta = select(Order).where(Order.user_id == user_id)
```

### Actualizar

Se implementó la actualización del nombre de un usuario:

```python
user.name = nuevo_nombre
session.commit()
```

### Eliminar

Se implementó la eliminación de elementos de una orden:

```python
session.delete(item)
session.commit()
```

## Transacciones y rollback

Las operaciones que modifican la base de datos deben confirmarse con:

```python
session.commit()
```

Si ocurre un error antes de completar la operación, se utiliza:

```python
session.rollback()
```

Esto revierte los cambios pendientes de la transacción.

Ejemplo:

```python
try:
    session.add(usuario)
    session.commit()
except Exception:
    session.rollback()
    raise
```

Se probó el rollback mediante un intento de insertar un usuario con un correo duplicado.

## Migraciones con Alembic

Alembic administra las modificaciones del esquema de la base de datos.

La configuración principal se encuentra en:

```text
alembic.ini
```

Los archivos de migración se encuentran en:

```text
migrations/versions/
```

### Metadatos

Alembic utiliza:

```python
target_metadata = Base.metadata
```

para comparar los modelos ORM con el esquema existente.

### Crear una revisión

```bash
poetry run alembic revision --autogenerate -m "Crea tablas iniciales"
```

La revisión inicial crea:

- `users`.
- `orders`.
- `order_items`.

También define las claves foráneas correspondientes.

### Aplicar migraciones

```bash
poetry run alembic upgrade head
```

`head` representa la revisión más reciente.

### Consultar la revisión actual

```bash
poetry run alembic current
```

### Consultar el historial

```bash
poetry run alembic history
```

### Comprobar cambios pendientes

```bash
poetry run alembic check
```

### Revertir una revisión

```bash
poetry run alembic downgrade -1
```

Las migraciones autogeneradas deben revisarse antes de aplicarse, especialmente cuando existen renombrados, transformaciones de datos o cambios complejos.

## SQLite en memoria para pruebas

Las pruebas utilizan:

```text
sqlite:///:memory:
```

La fixture ubicada en:

```text
tests/conftest.py
```

crea una base temporal para cada prueba.

El flujo de la fixture es:

```text
Crear engine en memoria
        ↓
Crear tablas
        ↓
Crear sesión
        ↓
Ejecutar la prueba
        ↓
Cerrar sesión
        ↓
Liberar engine
```

La base en memoria permite:

- Aislar las pruebas.
- Evitar modificar `app.db`.
- No depender de un servidor externo.
- Crear un estado limpio para cada prueba.

## Pruebas implementadas

Las pruebas se encuentran en:

```text
tests/test_repositorio.py
```

Se verificaron:

- Creación de un usuario.
- Consulta de un usuario.
- Creación de una orden.
- Asociación de elementos a una orden.
- Consulta de órdenes por usuario.
- Actualización de usuarios.
- Eliminación de elementos.
- Restricción de correo único.
- Rollback después de un error de integridad.

La suite se ejecuta con:

```bash
poetry run pytest -q
```

## Flujo principal

El archivo:

```text
src/main.py
```

ejecuta el flujo principal:

```text
Crear o aplicar el esquema
        ↓
Crear usuario
        ↓
Crear orden
        ↓
Agregar elemento
        ↓
Consultar órdenes del usuario
        ↓
Mostrar resultados
```

Para ejecutar el programa como módulo:

```bash
poetry run python -m src.main
```

Resultado esperado:

```text
Usuario: Ana
Órdenes: 1
```

## Errores manejados

Durante el laboratorio se trabajó con:

- Usuario inexistente.
- Orden inexistente.
- Elemento inexistente.
- Correo duplicado.
- Fallos de integridad.
- Rollback de transacciones.
- Consultas sin resultados.

## Diferencia entre `create_all` y Alembic

`Base.metadata.create_all(engine)` crea las tablas que no existen, pero no administra de forma completa la evolución de un esquema existente.

Alembic permite:

- Registrar cambios.
- Aplicar migraciones.
- Consultar versiones.
- Revertir cambios.
- Mantener un historial del esquema.

En este proyecto, `create_all` se utiliza para preparar las bases temporales de las pruebas, mientras Alembic administra la base local de desarrollo.

## Resultado del módulo

Se implementaron:

- Modelos ORM `User`, `Order` y `OrderItem`.
- Relaciones uno a muchos.
- Claves primarias y foráneas.
- Sesiones SQLAlchemy.
- Operaciones CRUD.
- Transacciones y rollback.
- Migración inicial con Alembic.
- Pruebas aisladas con SQLite en memoria.
- Consultas entre entidades relacionadas.
- Validación de restricciones de base de datos.