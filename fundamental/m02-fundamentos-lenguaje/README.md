# Módulo 02: Fundamentos del lenguaje

## Objetivo

Crear un script Python que lea información desde un archivo JSON, filtre y valide registros, agregue resultados y maneje errores de archivo, formato y estructura.

## Entorno

- Python 3.12
- Poetry
- Ambiente virtual `.venv`
- Black
- isort
- Ruff
- pre-commit
- Git local

## Estructura del proyecto

```text
m02-fundamentos-del-lenguaje/
├── .gitignore
├── .pre-commit-config.yaml
├── datos/
│   └── usuarios.json
├── poetry.lock
├── pyproject.toml
├── README.md
└── src/
    └── main.py
```

La carpeta `.venv/` se genera localmente y no debe versionarse. La carpeta `.ruff_cache/` también es generada por Ruff y se excluye mediante `.gitignore`.

## Datos de entrada

El archivo `datos/usuarios.json` contiene una lista de usuarios con los campos:

- `nombre`
- `correo`
- `rol`
- `activo`

Ejemplo:

```json
[
  {
    "nombre": "Ana",
    "correo": "ana@example.com",
    "rol": "admin",
    "activo": true
  }
]
```

## Funcionalidad implementada

El script `src/main.py` realiza las siguientes operaciones:

1. Construye la ruta del archivo JSON mediante `pathlib.Path`.
2. Abre el archivo usando un bloque `with`.
3. Convierte el contenido JSON a estructuras Python mediante `json.load`.
4. Maneja `FileNotFoundError` cuando el archivo no existe.
5. Maneja `json.JSONDecodeError` cuando el contenido no es un JSON válido.
6. Valida que el JSON contenga una lista.
7. Filtra usuarios activos.
8. Valida el formato de los correos con `re.fullmatch`.
9. Descarta registros incompletos o con correo inválido.
10. Agrupa los usuarios válidos por rol.
11. Muestra los usuarios filtrados y un resumen por rol.

## Ejecución

Desde la raíz del proyecto:

```bash
poetry run python src/main.py
```

Resultado esperado con los datos iniciales:

```text
Usuarios activos con correo válido:
- Ana: ana@example.com
- Carlos: carlos@example.com

Resumen por rol:
- admin: 1
- editor: 1
```

## Pruebas realizadas

Se verificaron los siguientes casos:

- Archivo JSON correcto.
- Archivo inexistente.
- JSON con formato inválido.
- JSON válido con una estructura distinta de una lista.
- Usuario activo con correo válido.
- Usuario activo con correo inválido.
- Usuario inactivo con correo válido.

## Herramientas de calidad

Formatear el código con Black:

```bash
poetry run black src
```

Comprobar el formato sin modificar archivos:

```bash
poetry run black --check src
```

Analizar el código con Ruff:

```bash
poetry run ruff check src
```

Aplicar correcciones automáticas compatibles:

```bash
poetry run ruff check src --fix
```

Ejecutar los hooks configurados:

```bash
poetry run pre-commit run --all-files
```

## Excepción local de isort

isort se instaló como dependencia de desarrollo y se configuró en `pyproject.toml`. Sin embargo, su ejecución permanece bloqueada por una política corporativa de Control de aplicaciones de Windows.

Por esta razón:

- No se ejecutó isort directamente.
- No se incluyó isort en los hooks de pre-commit.
- Ruff se utilizó para revisar las reglas relacionadas con imports.

Esta es una excepción local y temporal. Cuando el área de TI autorice su ejecución, deberá probarse nuevamente y considerarse su incorporación a pre-commit.

## Archivos generados localmente

Las siguientes carpetas no deben versionarse:

```text
.venv/
.ruff_cache/
__pycache__/
```

`.venv/` contiene el ambiente virtual y `.ruff_cache/` contiene información temporal utilizada por Ruff para acelerar análisis posteriores.