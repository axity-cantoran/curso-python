# Módulo Avanzado 02: CLI y automatización

## Descripción

Este módulo implementa una CLI con Typer para gestionar órdenes mediante una API HTTP protegida con JWT.

La CLI permite:

- Listar órdenes.
- Crear órdenes.
- Eliminar órdenes.
- Validar argumentos.
- Leer configuración desde variables de entorno.
- Gestionar errores HTTP.
- Utilizar un entry point instalable llamado `orders`.

## Objetivos

- Construir una CLI productiva y mantenible.
- Separar configuración, cliente HTTP y comandos.
- Integrar automatizaciones del proyecto.
- Utilizar variables de entorno.
- Gestionar códigos de salida y errores.
- Consumir una API protegida mediante JWT.

## Estructura del módulo

```text
m02-cli-automatizacion/
├── README.md
├── pyproject.toml
├── poetry.lock
├── src/
│   └── m02_cli_automatizacion/
│       ├── __init__.py
│       ├── cli.py
│       ├── client.py
│       └── config.py
└── tests/
    └── test_cli.py
```

El proyecto se configura como un paquete Python real mediante `src/m02_cli_automatizacion`.

## Dependencias

- Typer.
- `httpx`.
- pytest.

## Configuración mediante variables de entorno

La CLI utiliza:

```text
ORDERS_API_URL
ORDERS_API_TOKEN
ORDERS_API_TIMEOUT
```

Ejemplo:

```bash
export ORDERS_API_URL=http://localhost:8000
export ORDERS_API_TIMEOUT=10
export ORDERS_API_TOKEN="token-obtenido-de-la-api"
```

El token no debe incluirse en:

- Código fuente.
- README.
- Commits.
- Archivos de configuración versionados.
- Logs.

## Clase `Settings`

El módulo `config.py` contiene:

```python
@dataclass(frozen=True)
class Settings:
    api_url: str
    api_token: str | None
    timeout: float
```

`load_settings()`:

- Lee la URL de la API.
- Lee el token opcional.
- Lee el timeout.
- Valida la URL.
- Valida que el timeout sea mayor que cero.
- Elimina la barra final de la URL.

## Cliente HTTP

El módulo `client.py` contiene `OrdersApiClient`.

El cliente:

- Utiliza `httpx.Client`.
- Configura `base_url`.
- Aplica timeout.
- Envía el token como Bearer.
- Lista órdenes.
- Crea órdenes.
- Elimina órdenes.
- Lanza errores para respuestas HTTP no exitosas.
- Cierra el cliente después de utilizarlo.

Encabezado enviado:

```http
Authorization: Bearer <token>
```

## Comandos disponibles

El entry point se llama:

```text
orders
```

Ayuda general:

```bash
poetry run orders --help
```

### Listar órdenes

```bash
poetry run orders list
```

Consume:

```text
GET /orders/
```

### Crear una orden

```bash
poetry run orders create --product Teclado --quantity 2 --unit-price 50
```

Consume:

```text
POST /orders/
```

### Eliminar una orden

```bash
poetry run orders delete 1
```

Consume:

```text
DELETE /orders/1
```

## Validación de argumentos

Typer valida los parámetros de los comandos.

Ejemplo:

```bash
poetry run orders create --product Teclado --quantity 0 --unit-price 50
```

La cantidad se rechaza porque debe ser mayor o igual que uno.

También se valida que el identificador de una orden sea mayor que cero:

```bash
poetry run orders delete 0
```

## Códigos de salida

La CLI utiliza:

```text
0 → operación exitosa
1 → error durante la operación
```

Los errores se escriben en `stderr` y se controlan mediante errores específicos de HTTP y configuración.

## Entry point

El comando se registra en `pyproject.toml` mediante:

```toml
[project.scripts]
orders = "m02_cli_automatizacion.cli:app"
```

El proyecto utiliza modo de paquete para que Poetry instale correctamente el paquete y registre el comando.

La estructura requerida es:

```text
src/
└── m02_cli_automatizacion/
    ├── __init__.py
    ├── cli.py
    ├── client.py
    └── config.py
```

Los módulos internos utilizan imports relativos:

```python
from .client import OrdersApiClient
from .config import load_settings
```

## Pruebas

Las pruebas se encuentran en:

```text
tests/test_cli.py
```

Se verifican:

- Ayuda general.
- Validación de cantidades inválidas.
- Código de salida de errores.
- Comportamiento básico de la CLI.

Ejecutar las pruebas:

```bash
poetry run pytest tests -q
```

Resultado esperado:

```text
2 passed
```

## Pruebas manuales de integración

- Autenticación JWT.
- Listado de órdenes.
- Creación de órdenes.
- Eliminación de órdenes.
- Error `401 Unauthorized`.
- Errores de conexión.
- Validación local de argumentos.

## Integración con la API

La CLI consume la API de órdenes desarrollada previamente como dependencia funcional del laboratorio.

Para realizar las pruebas protegidas fue necesario:

1. Crear las tablas de la API.
2. Crear un usuario temporal:
   - Email: `ana@example.com`.
   - Contraseña: `secreto`.
3. Obtener un JWT mediante `/auth/login`.
4. Configurar `ORDERS_API_TOKEN`.
5. Ejecutar los comandos de la CLI.

El usuario temporal se utilizó únicamente para validar localmente la autenticación y el consumo de los endpoints. No debe incluirse como credencial real ni registrarse en el repositorio.

## Flujo de autenticación

```text
Usuario temporal
    ↓
POST /auth/login
    ↓
Obtener JWT
    ↓
Configurar ORDERS_API_TOKEN
    ↓
CLI envía Authorization: Bearer <token>
    ↓
API valida el token
    ↓
CLI procesa la respuesta
```

## Configuración de VS Code

Para resolver el paquete ubicado dentro de `src`, puede utilizarse:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "python.analysis.extraPaths": [
        "${workspaceFolder}/src"
    ]
}
```

Esta configuración solo afecta al editor y no contiene secretos.

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

Ejecutar pruebas:

```bash
poetry run pytest tests -q
```

Los hooks del repositorio consolidado se ejecutan desde la raíz de `curso-python`:

```bash
pre-commit run --all-files
```

## Problema del entry point

Inicialmente, el proyecto utilizaba:

```toml
[tool.poetry]
package-mode = false
```

y:

```toml
[tool.poetry.scripts]
orders = "src.cli:app"
```

Esta configuración permitía ejecutar el módulo directamente, pero no instalaba correctamente el comando `orders`.

La solución fue:

1. Crear el paquete `m02_cli_automatizacion`.
2. Mover `cli.py`, `client.py` y `config.py`.
3. Utilizar imports relativos.
4. Cambiar a `[project.scripts]`.
5. Configurar:

```toml
[project.scripts]
orders = "m02_cli_automatizacion.cli:app"
```

6. Regenerar `poetry.lock`.
7. Ejecutar `poetry install`.

Después de estos cambios funcionó:

```bash
poetry run orders --help
```

## Resultado del módulo

Se implementó una CLI Typer capaz de:

- Leer configuración desde variables de entorno.
- Consumir una API HTTP.
- Enviar autenticación Bearer.
- Listar órdenes.
- Crear órdenes.
- Eliminar órdenes.
- Validar argumentos.
- Gestionar errores HTTP y de configuración.
- Utilizar un entry point instalable llamado `orders`.
- Probar comandos básicos con pytest.