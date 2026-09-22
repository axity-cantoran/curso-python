# Módulo 03: Funciones y programación Pythonic

## Descripción

Este módulo presenta características fundamentales de la programación idiomática en Python:

- Funciones con argumentos posicionales y nombrados.
- `*args` y `**kwargs`.
- Funciones lambda.
- Closures.
- Decoradores.
- Iteradores y generadores.
- Comprensiones.
- Context managers.

El laboratorio integra decoradores, generadores y context managers en un flujo de procesamiento por lotes.

## Objetivos

- Diseñar funciones claras y expresivas.
- Utilizar argumentos variables.
- Implementar decoradores reutilizables.
- Crear generadores eficientes.
- Gestionar recursos y tareas de limpieza mediante context managers.
- Aplicar validaciones y manejo de excepciones.

## Entorno

- Python 3.12
- Poetry
- Ambiente virtual `.venv`
- Visual Studio Code
- Git Bash
- Black
- isort
- Ruff
- pre-commit
- Git local

## Configuración del proyecto

El proyecto utiliza Poetry para administrar el ambiente virtual y las herramientas de desarrollo.

El ambiente virtual se encuentra dentro del proyecto:

```text
.venv/
```

El proyecto se configuró con:

```toml
[tool.poetry]
package-mode = false
```

Esto indica que Poetry se utiliza como gestor de dependencias y herramientas, sin instalar el proyecto como un paquete Python.

## Estructura del proyecto

```text
m03-pythonic/
├── .git/
├── .gitignore
├── .pre-commit-config.yaml
├── .venv/
├── poetry.lock
├── pyproject.toml
├── README.md
└── src/
    ├── lotes.py
    ├── main.py
    ├── reintentos.py
    └── temporizador.py
```

### Archivos principales

- `src/lotes.py`: generador que divide una secuencia en lotes.
- `src/temporizador.py`: context manager para medir la duración de un bloque.
- `src/reintentos.py`: decorador configurable para reintentar operaciones.
- `src/main.py`: integración de los componentes.
- `pyproject.toml`: configuración del proyecto y sus herramientas.
- `.pre-commit-config.yaml`: hooks automáticos de calidad.
- `.gitignore`: archivos y carpetas excluidos de Git.

## Generador por lotes

Archivo:

```text
src/lotes.py
```

La función:

```python
def generar_lotes(datos, tamaño):
    ...
```

divide una secuencia en lotes utilizando `yield`.

### Validaciones

- `True` y `False` no se utilicen como tamaños.
- `tamaño` sea mayor que cero.

Ejemplos de valores inválidos:

```python
generar_lotes(datos, 0)
generar_lotes(datos, -1)
generar_lotes(datos, "2")
generar_lotes(datos, True)
```

### Ejemplo de resultado

Para:

```python
datos = [1, 2, 3, 4, 5]
```

y un tamaño de lote igual a `2`, el generador produce:

```text
[1, 2]
[3, 4]
[5]
```

El último lote puede contener menos elementos que el tamaño solicitado.

### Ventaja del generador

Los lotes se producen progresivamente. No es necesario construir y almacenar todos los lotes antes de comenzar el procesamiento.

## Context manager de temporización

Archivo:

```text
src/temporizador.py
```

El context manager:

```python
def medir_tiempo(nombre="Bloque"):
    ...
```

se utiliza así:

```python
with medir_tiempo("Procesamiento"):
    ...
```

### Funcionamiento

1. Registra el tiempo inicial con `perf_counter`.
2. Entrega el control al bloque `with` mediante `yield`.
3. Calcula la duración al finalizar.
4. Muestra el tiempo transcurrido.
5. Ejecuta la medición dentro de `finally`.

El uso de `finally` garantiza que la finalización se ejecute incluso si ocurre una excepción dentro del bloque.

## Decorador de reintentos

Archivo:

```text
src/reintentos.py
```

El decorador:

```python
def reintentar(
    intentos=3,
    espera_inicial=0.5,
    factor_backoff=2,
    excepciones=(Exception,),
):
    ...
```

permite reintentar automáticamente una función cuando ocurre una excepción configurada.

### Parámetros

- `intentos`: número máximo de ejecuciones.
- `espera_inicial`: tiempo antes del primer reintento.
- `factor_backoff`: multiplicador de la espera.
- `excepciones`: tipos de excepción que activan el reintento.

### Backoff progresivo

Con:

```python
espera_inicial=0.5
factor_backoff=2
```

las esperas son aproximadamente:

```text
0.5 segundos
1.0 segundos
2.0 segundos
```

### Uso de `*args` y `**kwargs`

La envoltura utiliza:

```python
def envoltura(*args, **kwargs):
    ...
```

Esto permite decorar funciones que reciben:

- Argumentos posicionales.
- Argumentos nombrados.
- Una combinación de ambos.

### Excepciones

Cuando se agotan los intentos, se utiliza `raise` para relanzar la última excepción.

El decorador no oculta el error final.

### Conservación de metadatos

Se utiliza:

```python
@wraps(funcion)
```

para conservar información de la función original, como:

- Nombre.
- Documentación.
- Metadatos útiles para depuración.

## Integración

Archivo:

```text
src/main.py
```

El flujo principal:

1. Crea una colección de datos de ejemplo.
2. Genera lotes de tamaño definido.
3. Procesa cada lote.
4. Simula un fallo temporal.
5. Reintenta automáticamente la operación.
6. Mide el tiempo total de procesamiento.

### Ejecución

Desde la raíz del proyecto:

```bash
poetry run python src/main.py
```

La salida esperada es similar a:

```text
Intento 1 fallido. Reintentando en 0.10 segundos...
Lote procesado: [1, 2, 3]
Lote procesado: [4, 5, 6]
Lote procesado: [7, 8, 9]
Lote procesado: [10]
Procesamiento total: 0.1005 segundos
```

El tiempo exacto puede variar según el equipo.

## Decisiones de implementación

La simulación utiliza una variable global para provocar un fallo temporal en la primera ejecución.

Esto permite demostrar el funcionamiento del decorador, pero no representa necesariamente el diseño recomendado para una aplicación real.

El uso de estado global puede:

- Compartir información entre llamadas.
- Dificultar las pruebas.
- Generar problemas en ejecuciones concurrentes.
- Hacer que una función dependa de información externa.

En una aplicación real, sería preferible encapsular el estado o utilizar una dependencia controlada.
