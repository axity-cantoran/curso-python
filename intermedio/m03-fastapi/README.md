# Módulo 03: APIs web con FastAPI

## Descripción

Este módulo implementa una API web para gestionar órdenes mediante FastAPI.

La API incluye:

- Estructura modular.
- Routers.
- Dependencias.
- Esquemas Pydantic.
- Validación de entradas.
- Documentación OpenAPI.
- CRUD de órdenes.
- Autenticación JWT.
- Protección de endpoints.
- Pruebas con base de datos temporal.

## Objetivos

- Exponer una API coherente y validada.
- Separar responsabilidades mediante routers, dependencias y servicios.
- Validar entradas y salidas con Pydantic.
- Documentar automáticamente los endpoints.
- Proteger rutas mediante autenticación JWT.
- Probar endpoints utilizando una base de datos temporal.

## Estructura del módulo

```text
m03-fastapi/
├── app/
│   ├── __init__.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── orders.py
│   └── services/
│       └── orders.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_orders.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Aplicación FastAPI

La aplicación principal se encuentra en:

```text
app/main.py
```

FastAPI se configura con:

- Título de la API.
- Versión.
- Routers.
- Endpoint de salud.
- Configuración de inicio.

Ejecutar la aplicación:

```bash
poetry run uvicorn app.main:app --reload
```

La API queda disponible en:

```text
http://127.0.0.1:8000
```

## Routers

Los endpoints se separan por responsabilidad:

### Router de autenticación

Archivo:

```text
app/routers/auth.py
```

Ruta principal:

```text
/auth
```

Incluye el endpoint de login.

### Router de órdenes

Archivo:

```text
app/routers/orders.py
```

Ruta principal:

```text
/orders
```

Incluye las operaciones CRUD de órdenes.

## Endpoint de salud

```text
GET /health
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

Este endpoint permite comprobar que la aplicación está funcionando.

## Esquemas Pydantic

Los esquemas se encuentran en:

```text
app/schemas.py
```

### `OrderCreate`

Representa los datos necesarios para crear una orden:

- `product`
- `quantity`
- `unit_price`

Validaciones:

- `product` no puede estar vacío.
- `quantity` debe ser mayor que cero.
- `unit_price` debe ser mayor que cero.

### `OrderUpdate`

Representa los datos que pueden modificarse. Sus campos son opcionales:

- `product`
- `quantity`
- `unit_price`

### `OrderOut`

Representa la respuesta de una orden:

- `id`
- `product`
- `quantity`
- `unit_price`

Utiliza:

```python
model_config = {
    "from_attributes": True,
}
```

Esto permite construir el esquema a partir de una entidad ORM.

### `Token`

Representa la respuesta del login:

```json
{
  "access_token": "token",
  "token_type": "bearer"
}
```

## Validación de entradas

FastAPI valida automáticamente los cuerpos JSON mediante Pydantic.

Ejemplo válido:

```json
{
  "product": "Teclado",
  "quantity": 2,
  "unit_price": 50.0
}
```

Ejemplo inválido:

```json
{
  "product": "",
  "quantity": 0,
  "unit_price": -10
}
```

Los datos inválidos producen:

```text
422 Unprocessable Entity
```

## CRUD de órdenes

Los endpoints disponibles son:

| Método | Ruta | Descripción | Respuesta principal |
|---|---|---|---|
| `POST` | `/orders/` | Crear una orden | `201 Created` |
| `GET` | `/orders/` | Listar órdenes | `200 OK` |
| `GET` | `/orders/{order_id}` | Consultar una orden | `200 OK` |
| `PUT` | `/orders/{order_id}` | Actualizar una orden | `200 OK` |
| `DELETE` | `/orders/{order_id}` | Eliminar una orden | `204 No Content` |

Una orden inexistente produce:

```text
404 Not Found
```

La respuesta contiene:

```json
{
  "detail": "Orden no encontrada"
}
```

## Modelos ORM y base de datos

Los modelos se encuentran en:

```text
app/models.py
```

Se utilizan las entidades relacionadas del módulo de acceso a datos (Módulo Intermedio 02):

- `User`.
- `Order`.
- Relaciones mediante SQLAlchemy.

La sesión de base de datos se proporciona mediante la dependencia:

```python
get_db
```

Durante las pruebas, esta dependencia se sustituye por una sesión conectada a SQLite en memoria.

## Dependencias de FastAPI

Las dependencias se encuentran en:

```text
app/dependencies.py
```

Se utilizan para:

- Proporcionar sesiones.
- Obtener el token Bearer.
- Validar el usuario actual.
- Proteger endpoints.

Ejemplo conceptual:

```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    ...
```

## Autenticación JWT

La seguridad se implementa en:

```text
app/security.py
```

El flujo es:

```text
Credenciales
    ↓
POST /auth/login
    ↓
Verificación del usuario
    ↓
Generación del JWT
    ↓
Authorization: Bearer <token>
    ↓
Acceso a endpoints protegidos
```

### Login

```text
POST /auth/login
```

El endpoint utiliza un formulario OAuth2 con:

```text
username
password
```

Ejemplo:

```text
username: ana@example.com
password: secreto
```

Una respuesta válida contiene:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Token

El token incluye información como:

- Identificador del usuario.
- Fecha de expiración.
- Firma de integridad.

El encabezado utilizado para solicitudes protegidas es:

```http
Authorization: Bearer <token>
```

### Respuestas de autenticación

| Código | Situación |
|---|---|
| `401 Unauthorized` | Credenciales ausentes o inválidas |
| `403 Forbidden` | Usuario autenticado sin permisos suficientes |

## Protección de órdenes

Los endpoints de órdenes utilizan la dependencia del usuario actual.

La API:

- Rechaza solicitudes sin token.
- Asocia nuevas órdenes al usuario autenticado.
- Solo permite consultar órdenes propias.
- Solo permite actualizar órdenes propias.
- Solo permite eliminar órdenes propias.

## Documentación OpenAPI

FastAPI genera documentación automáticamente.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Especificación OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

Swagger permite:

- Consultar rutas.
- Revisar esquemas.
- Ejecutar solicitudes.
- Probar autenticación.
- Ver códigos de respuesta.

## Testing de endpoints

Las pruebas se encuentran en:

```text
tests/
```

Se utiliza:

- `pytest`.
- `TestClient`.
- `pytest-asyncio`.
- `aiohttp`.
- Dependencias sobrescritas.
- SQLite en memoria.

### Base de datos temporal

La fixture de pruebas:

1. Crea un engine SQLite en memoria.
2. Crea las tablas.
3. Crea una sesión temporal.
4. Sobrescribe `get_db`.
5. Ejecuta la prueba.
6. Limpia las dependencias al finalizar.

La base temporal evita modificar la base de desarrollo.

### Pruebas de autenticación

Se comprueban:

- Login con contraseña incorrecta.
- Solicitudes sin token.
- Acceso con token válido.

### Pruebas de órdenes

Se comprueban:

- Creación de órdenes.
- Consulta de órdenes.
- Validación de datos.
- Respuestas `404`.
- Protección de endpoints.
- Relación entre usuario autenticado y orden.

## Comandos principales

Instalar dependencias:

```bash
poetry install
```

Iniciar la API:

```bash
poetry run uvicorn app.main:app --reload
```

Ejecutar pruebas:

```bash
poetry run pytest tests -q
```

Ejecutar pruebas con cobertura:

```bash
poetry run pytest tests --cov=app --cov-report=term-missing
```

Ejecutar mypy:

```bash
poetry run mypy app tests
```

Ejecutar Ruff:

```bash
poetry run ruff check app tests
```

Comprobar formato:

```bash
poetry run black --check app tests
```

Ejecutar pre-commit desde la raíz del repositorio:

```bash
pre-commit run --all-files
```

## Validación de calidad

Se utilizaron las herramientas configuradas en módulos anteriores, adaptadas al repositorio consolidado:

- Black.
- Ruff.
- mypy.
- pre-commit.

El hook de mypy requiere dependencias adicionales para analizar correctamente FastAPI, SQLAlchemy, Pydantic y las pruebas:

```yaml
additional_dependencies:
  - fastapi
  - sqlalchemy
  - pydantic
  - pytest
  - httpx
  - types-python-jose
  - types-passlib
```

isort permanece instalado y configurado, pero no se ejecuta por el bloqueo corporativo documentado.

## Incidencias relevantes

### Compatibilidad entre Passlib y bcrypt

Se fijó una versión compatible de `bcrypt` debido a un error de compatibilidad con Passlib:

```bash
poetry add "bcrypt==4.0.1"
```

### SQLite en memoria durante las pruebas

Se utilizó `StaticPool` para compartir la conexión de SQLite en memoria:

```python
poolclass=StaticPool
```

Esto evita que cada conexión cree una base distinta y permite que la aplicación y las pruebas utilicen las mismas tablas temporales.

## Resultado del módulo

Se implementó una API FastAPI que:

- Expone un endpoint de salud.
- Valida datos mediante Pydantic.
- Documenta rutas mediante OpenAPI.
- Implementa CRUD de órdenes.
- Gestiona sesiones de base de datos.
- Protege endpoints mediante JWT.
- Configura dependencias reutilizables.
- Utiliza SQLite temporal en pruebas.
- Comprueba login, validación y autorización mediante pruebas de integración.