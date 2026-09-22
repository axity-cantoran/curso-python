# Módulo 05: Tipado estático opcional y calidad

## Objetivo

Aplicar anotaciones de tipos y herramientas de análisis estático para mejorar la claridad, mantenibilidad y calidad del código Python.

## Contenidos aplicados

- Type hints.
- Tipos de parámetros y valores de retorno.
- Tipos opcionales.
- Configuración estricta de mypy.
- Análisis estático.
- Ruff.
- Black.
- Pre-commit.
- Checks de integración continua.
- Documentación de excepciones locales.

## Configuración de tipado

El proyecto utiliza Python 3.12 como versión objetivo.

La configuración de mypy se encuentra en `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
mypy_path = "src"
```

La opción `strict = true` habilita comprobaciones rigurosas sobre:

- Parámetros sin anotar.
- Valores de retorno.
- Tipos incompatibles.
- Valores potencialmente nulos.
- Imports y definiciones incompletas.

## Anotaciones implementadas

Se agregaron anotaciones en:

- Parámetros de funciones.
- Valores de retorno.
- Atributos.
- Métodos especiales.
- Funciones que pueden devolver `None`.

Ejemplos de formas utilizadas:

```python
def main() -> None:
    ...
```

```python
def convertir(valor: str) -> float:
    ...
```

```python
def buscar() -> str | None:
    ...
```

Las anotaciones documentan el contrato esperado y permiten que mypy y otras herramientas analicen el código.

## Verificación con mypy

Ejecutar mypy sobre el código fuente:

```bash
poetry run mypy src
```

Resultado esperado:

```text
Success: no issues found in 3 source files
```

mypy realiza análisis estático y no ejecuta las funciones. Detecta incompatibilidades de tipos antes de la ejecución, pero no sustituye la validación de datos externos ni las pruebas.

## Calidad de código

### Black

Formatear el código:

```bash
poetry run black src
```

Comprobar el formato sin modificar archivos:

```bash
poetry run black --check src
```

### Ruff

Analizar el código:

```bash
poetry run ruff check src
```

Aplicar correcciones automáticas compatibles:

```bash
poetry run ruff check src --fix
```

La configuración de Ruff se encuentra en `pyproject.toml` y contempla reglas de estilo, errores e imports.

## Pre-commit

La configuración se encuentra en:

```text
.pre-commit-config.yaml
```

Los hooks configurados son:

- Black.
- Ruff.
- Ruff Format.
- mypy.

Instalar el hook de Git:

```bash
poetry run pre-commit install
```

Ejecutar todos los hooks:

```bash
poetry run pre-commit run --all-files
```

Los hooks permiten detectar problemas antes de crear un commit.

## Check de integración continua

Se creó el workflow:

```text
.github/workflows/quality.yml
```

El workflow utiliza GitHub Actions y ejecuta:

1. Checkout del repositorio.
2. Configuración de Python 3.12.
3. Instalación de Poetry.
4. Instalación de dependencias.
5. Ejecución de mypy.
6. Ejecución de Ruff.
7. Comprobación de Black.

El check se ejecuta en eventos de `push` y `pull_request`.

Para que se ejecute, el proyecto debe estar publicado en un repositorio remoto compatible con GitHub Actions.

## Excepción local de isort

isort está instalado y configurado en `pyproject.toml`, pero su ejecución está bloqueada por una política corporativa de Control de aplicaciones de Windows.

Por esta razón:

- No se ejecutó isort directamente.
- No se agregó isort a los hooks de pre-commit.
- Ruff revisa provisionalmente las reglas relacionadas con imports.
- La configuración de isort se conserva para una futura validación.

Esta excepción es local y temporal. Cuando se autorice su ejecución, deberá verificarse nuevamente y evaluarse su incorporación a pre-commit.

## Archivos excluidos de Git

El archivo `.gitignore` excluye:

```text
.venv/
__pycache__/
*.py[cod]
.ruff_cache/
.pytest_cache/
.mypy_cache/
```

Estas rutas contienen ambientes virtuales, cachés o archivos generados localmente.

## Estructura relacionada con este módulo

```text
m05-tipado-calidad/
├── .github/
│   └── workflows/
│       └── quality.yml
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
└── src/
```

## Resultado

En este módulo se logró:

- Anotar el código con tipos.
- Configurar mypy en modo estricto.
- Verificar el código estáticamente.
- Aplicar Black y Ruff.
- Automatizar validaciones con pre-commit.
- Crear un check básico de CI.
- Documentar la excepción local de isort.