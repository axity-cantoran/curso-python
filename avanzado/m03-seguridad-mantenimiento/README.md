```markdown
# Módulo Avanzado 03: Seguridad y mantenimiento

## Descripción

Este módulo aplica prácticas de seguridad y mantenimiento a un proyecto Python mediante:

- Gestión tipada de configuración.
- Separación de secretos.
- Auditoría de dependencias.
- Control de versiones.
- Hardening del runtime.
- Hardening de contenedores Docker.

## Objetivos

- Proteger secretos y configuraciones sensibles.
- Auditar dependencias instaladas.
- Mantener versiones compatibles.
- Reducir la superficie de ataque.
- Ejecutar contenedores con privilegios mínimos.
- Validar configuraciones inseguras antes de iniciar la aplicación.

## Estructura del módulo

```text
m03-seguridad-mantenimiento/
├── .dockerignore
├── .env.example
├── Dockerfile
├── README.md
├── poetry.lock
├── pyproject.toml
└── src/
    ├── __init__.py
    ├── config.py
    └── main.py
```

El archivo `.env` se utiliza únicamente de forma local y no debe versionarse.

## Configuración tipada

La configuración se implementa mediante `pydantic-settings`.

El módulo `src/config.py` define:

```python
class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    service_url: str = "http://localhost:8000"
    api_token: str
    debug: bool = False
    timeout: float = Field(default=10.0, gt=0)
```

### Variables utilizadas

```text
APP_ENV
LOG_LEVEL
SERVICE_URL
API_TOKEN
DEBUG
TIMEOUT
```

### Archivo `.env.example`

El repositorio contiene `.env.example` como referencia:

```text
APP_ENV=development
LOG_LEVEL=INFO
SERVICE_URL=http://localhost:8000
API_TOKEN=replace-with-a-local-secret
DEBUG=false
TIMEOUT=10
```

Este archivo no contiene secretos reales.

### Archivo `.env`

El archivo `.env` se utiliza localmente para proporcionar valores reales de desarrollo:

```text
API_TOKEN=local-development-token
```

No debe subirse al repositorio.

## Validación del runtime

La aplicación valida la configuración antes de iniciar.

En producción:

- `debug` no puede estar activo.
- `api_token` debe estar configurado.
- El timeout debe ser mayor que cero.
- La URL debe tener un protocolo válido.

Una configuración insegura impide el inicio de la aplicación.

Este comportamiento aplica el principio de **fallar de forma segura**.

## Ejecución local

Desde la raíz del módulo:

```bash
poetry run python -m src.main
```

Resultado esperado:

```text
Configuración válida
```

El token no se imprime; únicamente se comprueba que esté configurado.

## Auditoría de dependencias

### pip-audit

Ejecutar:

```bash
poetry run pip-audit
```

`pip-audit` revisa las dependencias instaladas y las compara con vulnerabilidades conocidas.

### Safety

El módulo conserva Safety como herramienta de auditoría:

```bash
poetry run safety scan
```

La versión utilizada requiere autenticación para completar el escaneo.

## Hallazgo de seguridad

`pip-audit` detectó:

```text
Paquete: nltk
Versión: 3.10.3
Vulnerabilidad: PYSEC-2026-3740
```

El paquete `nltk` es una dependencia transitiva de:

```text
safety 3.8.1
```

No es una dependencia directa de la aplicación.

Se intentó actualizar Safety, pero la resolución no cambió y `nltk` permaneció en la misma versión.

### Limitación de Safety

La ejecución de:

```bash
poetry run safety scan
```

solicitó iniciar sesión o registrarse. El proceso se interrumpió sin crear una cuenta.

Por esta razón:

- `pip-audit` se utiliza como auditoría principal.
- El hallazgo de `nltk` queda documentado.
- Safety permanece instalado porque forma parte de los requisitos del módulo.
- La limitación de autenticación queda registrada.
- El hallazgo debe revisarse nuevamente cuando exista una versión corregida o una alternativa compatible.

## Versiones y compatibilidad

Las dependencias se gestionan mediante:

```text
pyproject.toml
poetry.lock
```

El archivo `pyproject.toml` define las restricciones de versión y `poetry.lock` conserva la resolución concreta.

Las actualizaciones deben realizarse mediante este flujo:

```text
Auditar
    ↓
Identificar dependencia vulnerable
    ↓
Revisar versión corregida
    ↓
Evaluar compatibilidad
    ↓
Actualizar de forma controlada
    ↓
Ejecutar pruebas
    ↓
Auditar nuevamente
```

No se deben actualizar dependencias automáticamente sin comprobar compatibilidad y resultados de auditoría.

## Dockerfile endurecido

El `Dockerfile` aplica las siguientes medidas:

- Imagen base `python:3.12-slim`.
- Variables para evitar bytecode y salida retrasada.
- Usuario no root.
- Instalación de dependencias de producción.
- Eliminación de Poetry después de instalar.
- Permisos ajustados al usuario de aplicación.
- Ejecución con privilegios mínimos.

Fragmento principal:

```dockerfile
RUN useradd --create-home --shell /usr/sbin/nologin appuser

WORKDIR /app

USER appuser
```

La aplicación no se ejecuta como `root`.

## `.dockerignore`

El archivo `.dockerignore` excluye:

```text
.env
.git
.venv
__pycache__
.pytest_cache
.ruff_cache
.mypy_cache
tests
*.pyc
```

Esto evita incluir en la imagen:

- Secretos.
- Historial Git.
- Ambientes virtuales.
- Cachés.
- Pruebas.
- Archivos temporales.

## Construir la imagen

```bash
docker build \
  -t m03-seguridad-mantenimiento:local \
  .
```

Para reconstruir ignorando la caché:

```bash
docker build --no-cache \
  -t m03-seguridad-mantenimiento:local \
  .
```

## Ejecutar el contenedor

```bash
docker run --rm \
  --env-file .env \
  m03-seguridad-mantenimiento:local
```

## Verificar el usuario

```bash
docker run --rm \
  m03-seguridad-mantenimiento:local \
  id
```

La aplicación debe ejecutarse como `appuser`, no como `root`.

## Ejecutar con hardening adicional

```bash
docker run --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --env-file .env \
  m03-seguridad-mantenimiento:local
```

### Medidas aplicadas

| Medida | Riesgo reducido |
|---|---|
| Usuario no root | Escalada de privilegios |
| Imagen `slim` | Superficie de ataque |
| `--read-only` | Escrituras no autorizadas |
| `--cap-drop=ALL` | Capacidades excesivas |
| `no-new-privileges` | Obtención de privilegios adicionales |
| `.dockerignore` | Exposición de secretos y archivos locales |

## Validación de calidad

Ejecutar Ruff:

```bash
poetry run ruff check src
```

Comprobar el formato:

```bash
poetry run black --check src
```

Ejecutar mypy:

```bash
poetry run mypy src
```

Los hooks del repositorio consolidado se ejecutan desde la raíz de `curso-python`:

```bash
pre-commit run --all-files
```

## Archivos que no deben versionarse

No deben incluirse en Git:

```text
.env
.venv/
__pycache__/
.ruff_cache/
.mypy_cache/
```

El archivo `.env.example` sí puede versionarse porque no contiene secretos reales.

## Resultado del módulo

Se implementó un proyecto con:

- Configuración tipada mediante `pydantic-settings`.
- Separación de secretos mediante variables de entorno.
- Auditoría con `pip-audit` y Safety.
- Gestión controlada de versiones.
- Documentación de una vulnerabilidad transitiva.
- Imagen Docker con usuario no root.
- Permisos mínimos.
- Contenedor de solo lectura.
- Capacidades eliminadas.
- Protección contra nuevos privilegios.
```