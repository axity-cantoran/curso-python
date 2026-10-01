# PROYECTO FINAL: ORDERS

## Descripción

Servicio de órdenes para una tienda de figuras de acción, desarrollado con Arquitectura Hexagonal y principios de Arquitectura Limpia.

Incluye:

- Dominio, aplicación, puertos y adaptadores.
- API FastAPI protegida mediante API key.
- Persistencia SQLite con SQLAlchemy.
- Migraciones Alembic.
- Pruebas unitarias, de contrato, integración y E2E.
- Ruff, mypy y cobertura.
- Auditoría de dependencias.
- Docker multistage.
- CI con GitHub Actions.

## Catálogo

El catálogo se define directamente en el código y contiene seis productos:

| Identificador | Nombre | Categoría |
|---|---|---|
| `caballero` | Caballero | Figuras |
| `mago` | Mago | Figuras |
| `robot` | Robot | Figuras |
| `alienigena` | Alienígena | Figuras |
| `accesorios` | Accesorios | Complementos |
| `herramientas` | Herramientas | Complementos |

Las órdenes pueden contener varios productos.

## Estados

```text
PENDING
CONFIRMED
CANCELLED
```

Transiciones permitidas:

```text
PENDING → CONFIRMED
PENDING → CANCELLED
```

Solo las órdenes `PENDING` pueden eliminarse.

## Estructura

```text
final-orders/
├── .dockerignore
├── .env.example
├── Dockerfile
├── docker-entrypoint.sh
├── README.md
├── alembic.ini
├── poetry.lock
├── pyproject.toml
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── src/
│   └── orders_api/
│       ├── main.py
│       ├── api/
│       ├── application/
│       ├── domain/
│       └── infrastructure/
└── tests/
    ├── conftest.py
    ├── contract/
    ├── e2e/
    ├── integration/
    └── unit/
```

El workflow se encuentra en la raíz del repositorio:

```text
.github/workflows/final-orders-ci.yml
```

## Arquitectura

```text
Cliente HTTP
    ↓
FastAPI
    ↓
Casos de uso
    ↓
Puerto de repositorio
    ↓
Adaptador SQLAlchemy
    ↓
SQLite
```

El dominio no depende de FastAPI, SQLAlchemy ni SQLite.

### Capas

- **Dominio:** entidades, estados, catálogo y reglas de negocio.
- **Aplicación:** casos de uso, comandos y puertos.
- **Infraestructura:** configuración, base de datos, modelos y repositorios.
- **API:** rutas, esquemas, dependencias y autenticación.

## Dependencias

### Producción

```text
fastapi
uvicorn
pydantic-settings
sqlalchemy
alembic
```

### Desarrollo

```text
pytest
httpx
ruff
mypy
pytest-cov
pip-audit
```

La versión de Poetry utilizada en el proyecto, Docker y CI es:

```text
2.4.3
```

El paquete se encuentra dentro de `src`:

```toml
[tool.poetry]
packages = [
    { include = "orders_api", from = "src" }
]
```

## Configuración

Archivo de referencia:

```text
.env.example
```

Contenido:

```env
DATABASE_URL=sqlite:///./orders.db
API_KEY=local-development-key
ENVIRONMENT=development
```

El archivo `.env` puede utilizarse localmente, pero no debe versionarse.

## Instalación y ejecución

Desde la carpeta del proyecto:

```bash
poetry install
poetry run alembic upgrade head
poetry run uvicorn orders_api.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

Documentación OpenAPI:

```text
http://localhost:8000/docs
```

## API

### Healthcheck

```http
GET /health
```

No requiere autenticación.

Respuesta:

```json
{"status":"ok"}
```

### Crear una orden

```http
POST /orders
```

Cabecera:

```text
X-API-Key: local-development-key
```

Cuerpo:

```json
{
  "items": [
    {
      "product_id": "caballero",
      "quantity": 1
    },
    {
      "product_id": "accesorios",
      "quantity": 2
    }
  ]
}
```

Respuesta:

```text
201 Created
```

### Listar órdenes

```http
GET /orders
```

### Consultar una orden

```http
GET /orders/{order_id}
```

### Cambiar el estado

```http
PATCH /orders/{order_id}/status
```

Confirmar:

```json
{
  "status": "CONFIRMED"
}
```

Cancelar:

```json
{
  "status": "CANCELLED"
}
```

### Eliminar una orden

```http
DELETE /orders/{order_id}
```

Solo se eliminan órdenes pendientes.

Respuestas principales:

```text
204 No Content
400 Bad Request
404 Not Found
```

Los endpoints de órdenes requieren:

```text
X-API-Key: local-development-key
```

## Migraciones

Aplicar migraciones:

```bash
poetry run alembic upgrade head
```

Consultar el estado:

```bash
poetry run alembic current
```

Crear una migración:

```bash
poetry run alembic revision --autogenerate -m "describe el cambio"
```

La base de datos local es:

```text
orders.db
```

No debe versionarse.

## Pruebas y calidad

Ejecutar toda la suite:

```bash
poetry run pytest
```

Ejecutar cobertura:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

La cobertura obtenida fue aproximadamente:

```text
93 %
```

Ejecutar Ruff:

```bash
poetry run ruff check src tests
```

Ejecutar mypy:

```bash
poetry run mypy src/orders_api
```

Ejecutar auditoría:

```bash
poetry run pip-audit
```

La auditoría final no detectó vulnerabilidades.

Puede aparecer una advertencia externa relacionada con Starlette, AnyIO y `TestClient`; no afecta a las pruebas cuando estas finalizan correctamente.

## Docker

La imagen utiliza una construcción multistage:

```text
builder
runtime
```

Características:

- Python 3.12.
- Poetry 2.4.3.
- Dependencias de producción.
- Migraciones Alembic.
- Usuario no root.
- Script de entrada.
- Imagen final reducida.

Construir:

```bash
docker build -t final-orders:local .
```

Ejecutar:

```bash
docker run --rm -p 8000:8000 \
  -e API_KEY=local-development-key \
  -e DATABASE_URL=sqlite:///./orders.db \
  final-orders:local
```

El script `docker-entrypoint.sh` ejecuta las migraciones antes de iniciar Uvicorn.

Probar:

```bash
curl http://localhost:8000/health
```

```bash
curl -H "X-API-Key: local-development-key" \
  http://localhost:8000/orders
```

## CI/CD

El workflow se encuentra en:

```text
.github/workflows/final-orders-ci.yml
```

El pipeline utiliza:

```yaml
working-directory: final-orders
```

y ejecuta:

- Instalación de dependencias.
- Ruff.
- Mypy.
- Pytest.
- Cobertura.
- Pip-audit.
- Construcción del paquete.
- Construcción de Docker.

Flujo:

```text
Instalar dependencias
    ↓
Lint
    ↓
Type-check
    ↓
Tests y cobertura
    ↓
Auditoría
    ↓
Build del paquete
    ↓
Build de Docker
```

El trabajo de Docker depende del trabajo de calidad:

```yaml
needs: quality
```

## Seguridad

La API key se configura mediante una variable de entorno:

```env
API_KEY=local-development-key
```

No deben versionarse:

```text
.env
.venv/
*.db
__pycache__/
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
htmlcov/
dist/
```

La aplicación del contenedor se ejecuta como:

```text
appuser
```

No se ejecuta como `root`.

## Problemas principales y soluciones

- **Mypy detectaba módulos duplicados:** se configuró `orders_api` como paquete dentro de `src` y se utilizó `explicit_package_bases`.
- **Ruff detectaba `Depends(...)`:** se ignoró `B008` únicamente en los archivos de FastAPI correspondientes.
- **SQLite en memoria no encontraba tablas:** se utilizó `StaticPool` en las pruebas.
- **El contenedor no tenía tablas:** `docker-entrypoint.sh` ejecuta Alembic antes de iniciar la aplicación.
- **Poetry tenía versiones diferentes:** se unificó Poetry en `2.4.3`.
- **Pip-audit detectó una vulnerabilidad en pytest:** se actualizó a `pytest >=9.0.3,<10.0.0`.
- **La wheel o la imagen utilizaban rutas incorrectas:** se configuró el directorio `final-orders` en las herramientas y el workflow.

### Compatibilidad de finales de línea

El archivo `docker-entrypoint.sh` debe conservar finales de línea `LF` para ejecutarse correctamente dentro de contenedores Linux.

Como el desarrollo se realiza en Windows, se añadió `.gitattributes` para mantener el formato adecuado:

```gitattributes
*.sh text eol=lf

## Resultado

El proyecto implementa un servicio funcional de órdenes con:

- Arquitectura Hexagonal.
- Catálogo fijo de seis productos.
- API FastAPI segura.
- Persistencia SQLite.
- Migraciones Alembic.
- Pruebas unitarias, de contrato, integración y E2E.
- Cobertura aproximada del 93 %.
- Ruff y mypy.
- Auditoría de dependencias.
- Docker multistage.
- Ejecución como usuario no root.
- CI automatizado con GitHub Actions.