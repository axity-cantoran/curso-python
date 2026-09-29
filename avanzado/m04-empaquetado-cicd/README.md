# Módulo Avanzado 04: Empaquetado, distribución y CI/CD

## Descripción

Este módulo empaqueta una aplicación FastAPI como distribución Python y automatiza su validación, construcción y publicación mediante:

- Poetry.
- Wheel.
- Distribución fuente.
- Docker multistage.
- GitHub Actions.
- GitHub Container Registry.

## Objetivos

- Crear un paquete Python distribuible.
- Generar una wheel y una distribución fuente.
- Validar el paquete en un entorno limpio.
- Construir una imagen Docker multistage.
- Ejecutar la aplicación con un usuario no root.
- Automatizar lint, type-check, tests y build.
- Publicar artefactos e imágenes de forma segura.

## Estructura del módulo

```text
m04-empaquetado-cicd/
├── .dockerignore
├── Dockerfile
├── README.md
├── poetry.lock
├── pyproject.toml
├── src/
│   └── orders_api/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_health.py
```

El workflow de GitHub Actions se encuentra en la raíz del repositorio:

```text
.github/
└── workflows/
    └── ci.yml
```

Esto es necesario porque GitHub Actions solo detecta workflows dentro de `.github/workflows/` en la raíz del repositorio.

## Aplicación FastAPI

La aplicación expone el endpoint:

```text
GET /health
```

La respuesta esperada es:

```json
{"status":"ok"}
```

La documentación interactiva está disponible en:

```text
http://localhost:8000/docs
```

## Empaquetado con Poetry

Las dependencias y los metadatos del paquete se definen en:

```text
pyproject.toml
```

La resolución concreta de dependencias se conserva en:

```text
poetry.lock
```

Instalar las dependencias:

```bash
poetry install
```

Comprobar la configuración:

```bash
poetry check
```

## Construcción de la distribución

Generar la wheel y la distribución fuente:

```bash
poetry build
```

Los archivos se generan en `dist/`:

```text
orders_api-0.1.0-py3-none-any.whl
orders_api-0.1.0.tar.gz
```

La wheel contiene:

- Código del paquete.
- Metadatos.
- Versión.
- Dependencias declaradas.

La carpeta `dist/` está excluida mediante `.gitignore`, ya que las distribuciones se generan localmente y en GitHub Actions.

## Validar la wheel

Crear un entorno temporal:

```bash
python -m venv .venv-wheel-test
```

Activarlo desde Git Bash:

```bash
source .venv-wheel-test/Scripts/activate
```

Instalar la wheel:

```bash
python -m pip install --upgrade pip
python -m pip install dist/orders_api-0.1.0-py3-none-any.whl
```

Comprobar la importación del paquete:

```bash
python -c "import orders_api; print(orders_api.__file__)"
```

Comprobar la aplicación:

```bash
python -c "from orders_api.main import app; print(app.title)"
```

Al finalizar:

```bash
deactivate
rm -rf .venv-wheel-test
```

Estos comandos deben ejecutarse desde la raíz del módulo:

```text
avanzado/m04-empaquetado-cicd
```

## Validación de calidad

Ejecutar las pruebas:

```bash
poetry run pytest
```

Ejecutar Ruff:

```bash
poetry run ruff check .
```

Ejecutar mypy:

```bash
poetry run mypy src
```

El resultado de las pruebas fue:

```text
1 passed, 1 warning
```

La advertencia procede de una dependencia externa relacionada con FastAPI, Starlette y httpx. No impide continuar porque la prueba finaliza correctamente.

## Docker multistage

El `Dockerfile` utiliza dos etapas:

```text
builder
runtime
```

### Etapa `builder`

Esta etapa:

- Instala Poetry.
- Copia `pyproject.toml` y `poetry.lock`.
- Instala las dependencias principales.
- Crea el entorno virtual dentro del proyecto.

La configuración:

```dockerfile
poetry config virtualenvs.in-project true
```

genera el entorno virtual en:

```text
/build/.venv
```

### Etapa `runtime`

La etapa final:

- Utiliza una imagen `python:3.12-slim`.
- Copia únicamente el entorno virtual necesario.
- Copia el código de la aplicación.
- Utiliza un usuario no root.
- Expone el puerto 8000.
- Ejecuta Uvicorn.

La variable:

```dockerfile
ENV PYTHONPATH="/app/src"
```

permite localizar el paquete copiado en:

```text
/app/src/orders_api
```

## `.dockerignore`

El archivo `.dockerignore` evita incluir en el contexto de construcción archivos innecesarios, como:

```text
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.mypy_cache/
dist/
.git/
```

Esto reduce el tamaño del contexto y evita copiar archivos generados o locales.

## Construir la imagen

Desde la raíz del módulo:

```bash
docker build -t orders-api:local .
```

Para ignorar la caché:

```bash
docker build --no-cache -t orders-api:local .
```

## Ejecutar el contenedor

```bash
docker run --rm -p 8000:8000 orders-api:local
```

Probar el endpoint desde otra terminal:

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{"status":"ok"}
```

Para detener el contenedor:

```text
Ctrl+C
```

## GitHub Actions

El workflow se encuentra en:

```text
.github/workflows/ci.yml
```

Como el proyecto forma parte de un monorepositorio, los pasos de Poetry y Docker utilizan:

```yaml
working-directory: avanzado/m04-empaquetado-cicd
```

### Validaciones ejecutadas

El workflow realiza:

- Instalación de Python 3.12.
- Instalación de Poetry.
- Instalación de dependencias.
- Lint con Ruff.
- Type-check con mypy.
- Tests con pytest.
- Construcción de la wheel.
- Construcción de la distribución fuente.
- Publicación del artefacto.
- Construcción de la imagen Docker.

### Artefacto generado

El workflow publica:

```text
orders-api-distributions
```

Este artefacto contiene:

```text
orders_api-0.1.0-py3-none-any.whl
orders_api-0.1.0.tar.gz
```

Puede descargarse desde la ejecución correspondiente en la pestaña **Actions** de GitHub.

## GitHub Container Registry

La imagen se publica en:

```text
ghcr.io/USUARIO/orders-api
```

`USUARIO` representa el propietario del repositorio y debe escribirse en minúsculas.

La autenticación utiliza:

```text
secrets.GITHUB_TOKEN
```

El workflow declara los permisos necesarios:

```yaml
permissions:
  contents: read
  packages: write
```

La imagen puede descargarse con:

```bash
docker pull ghcr.io/USUARIO/orders-api:latest
```

Ejecutarla:

```bash
docker run --rm -p 8000:8000 ghcr.io/USUARIO/orders-api:latest
```

Probarla:

```bash
curl http://localhost:8000/health
```

El workflow genera etiquetas basadas en:

- Rama.
- Pull request.
- Commit.
- `latest` para la rama predeterminada.

## Seguridad

No se incluyen credenciales en el repositorio.

No deben versionarse:

```text
.env
.venv/
dist/
*.pem
*.key
credentials.json
secrets.json
```

Tampoco deben escribirse tokens directamente en:

- El código fuente.
- El `Dockerfile`.
- El workflow.
- Los archivos de configuración.

La publicación utiliza el token automático de GitHub:

```text
secrets.GITHUB_TOKEN
```

## Flujo completo

```text
Preparar el paquete
    ↓
Construir la wheel
    ↓
Ejecutar tests
    ↓
Ejecutar lint
    ↓
Ejecutar type-check
    ↓
Construir la imagen Docker
    ↓
Probar el contenedor
    ↓
Publicar el artefacto
    ↓
Etiquetar la imagen
    ↓
Publicar la imagen en GHCR
```

## Problemas y soluciones

### Poetry no encontraba `/build/.venv`

Se añadió:

```dockerfile
poetry config virtualenvs.in-project true
```

Esto obligó a Poetry a crear el entorno virtual dentro del directorio del proyecto.

### Python no encontraba `orders_api`

El código se encontraba en:

```text
/app/src/orders_api
```

Se añadió:

```dockerfile
ENV PYTHONPATH="/app/src"
```

### GitHub Actions no encontraba `pyproject.toml`

El workflow se ejecutaba desde la raíz del repositorio. Se configuró:

```yaml
working-directory: avanzado/m04-empaquetado-cicd
```

en los pasos correspondientes.

### GitHub Actions no detectaba el workflow

El archivo se trasladó desde la carpeta del módulo a:

```text
.github/workflows/ci.yml
```

Esta es la ubicación que GitHub Actions reconoce en un monorepositorio.

### Advertencia durante las pruebas

Pytest mostró una advertencia externa relacionada con FastAPI, Starlette y httpx. La prueba pasó correctamente y no fue necesario modificar la configuración del laboratorio.

## Resultado del módulo

Se implementó un proyecto con:

- Aplicación FastAPI funcional.
- Paquete Python distribuible.
- Wheel y distribución fuente.
- Validación en un entorno limpio.
- Imagen Docker multistage.
- Usuario no root.
- Endpoint `/health` operativo.
- Lint, type-check y tests automatizados.
- Workflow de GitHub Actions.
- Artefacto descargable.
- Imagen publicada en GitHub Container Registry.
- Gestión segura de credenciales.