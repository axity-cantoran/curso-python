# Módulo 04: Concurrencia y rendimiento

## Descripción

Este módulo compara distintos modelos de ejecución para tareas de entrada/salida y procesamiento intensivo de CPU.

El laboratorio implementa:

- Un fetcher HTTP síncrono.
- Un fetcher HTTP asíncrono.
- Un límite de concurrencia mediante `asyncio.Semaphore`.
- Un cálculo CPU-bound secuencial.
- Un cálculo CPU-bound con `ProcessPoolExecutor`.
- Mediciones de rendimiento con `perf_counter`.
- Perfilado básico con `cProfile`.

## Objetivos

- Diferenciar tareas I/O-bound y CPU-bound.
- Comprender las implicaciones del GIL.
- Utilizar concurrencia asíncrona para operaciones de red.
- Controlar la cantidad de tareas simultáneas.
- Utilizar procesos para cálculos intensivos.
- Medir y comparar tiempos de ejecución.
- Interpretar información básica de perfilado.

## Estructura del módulo

```text
m04-concurrencia-rendimiento/
├── README.md
├── pyproject.toml
└── src/
    ├── cpu_bound.py
    ├── fetcher_async.py
    ├── fetcher_sync.py
    └── main.py
```

## Tareas I/O-bound y CPU-bound

### I/O-bound

Son tareas que pasan una parte importante del tiempo esperando operaciones externas:

- Solicitudes HTTP.
- Lectura y escritura de archivos.
- Consultas a bases de datos.
- Comunicación con servicios externos.

Para este tipo de tareas se utilizan principalmente:

```text
asyncio
httpx.AsyncClient
threading
ThreadPoolExecutor
```

### CPU-bound

Son tareas que utilizan principalmente el procesador:

- Cálculos numéricos.
- Compresión.
- Procesamiento de imágenes.
- Análisis intensivo de datos.

Para estas tareas se pueden utilizar:

```text
multiprocessing
ProcessPoolExecutor
```

## GIL

El Global Interpreter Lock es un mecanismo de CPython que permite que un solo hilo ejecute bytecode Python a la vez dentro de un proceso.

Sus principales implicaciones son:

- Los hilos no suelen proporcionar paralelismo real para código Python CPU-bound.
- Los hilos siguen siendo útiles para tareas I/O-bound.
- Los procesos permiten utilizar intérpretes independientes.
- `ProcessPoolExecutor` es una alternativa para cálculos intensivos.

## Fetcher síncrono

El archivo:

```text
src/fetcher_sync.py
```

contiene la función:

```python
def fetch_urls_sync(
    urls: list[str],
    timeout: float = 10.0,
) -> list[dict[str, object]]:
    ...
```

La función:

- Utiliza `httpx.Client`.
- Procesa las URLs una después de otra.
- Mide el tiempo de cada solicitud.
- Registra el código de respuesta.
- Conserva los errores individuales.
- Devuelve una lista de resultados.

Flujo:

```text
URL A → esperar respuesta
URL B → esperar respuesta
URL C → esperar respuesta
```

## Fetcher asíncrono

El archivo:

```text
src/fetcher_async.py
```

utiliza:

```python
httpx.AsyncClient
asyncio.gather
asyncio.Semaphore
```

La función principal es:

```python
async def fetch_urls_async(
    urls: list[str],
    limite_concurrencia: int = 5,
    timeout: float = 10.0,
) -> list[dict[str, object]]:
    ...
```

La versión asíncrona permite que varias solicitudes avancen durante sus tiempos de espera.

## Semáforo

El semáforo limita la cantidad de solicitudes simultáneas:

```python
semaforo = asyncio.Semaphore(limite_concurrencia)
```

Si el límite es `2`, solo dos coroutines pueden acceder al bloque protegido al mismo tiempo:

```text
A y B → activas
C, D y E → esperando
```

Cuando una solicitud termina, libera el permiso y otra coroutine puede continuar.

El semáforo ayuda a evitar:

- Saturación del servidor.
- Exceso de conexiones.
- Respuestas `429`.
- Consumo excesivo de recursos.

## Comparación de tiempos

El archivo:

```text
src/main.py
```

compara las versiones síncrona y asíncrona utilizando:

```python
from time import perf_counter
```

El flujo de medición es:

```text
Registrar tiempo inicial
        ↓
Ejecutar función
        ↓
Calcular tiempo transcurrido
```

La comparación realizada mostró que la versión asíncrona fue más rápida que la síncrona en las ejecuciones realizadas, con diferencias aproximadas de entre `0.08` y `0.2` segundos.

Los resultados pueden variar por:

- Latencia de red.
- Carga del servidor.
- Cachés.
- Resolución DNS.
- Límite de concurrencia.
- Condiciones del equipo.

## Cálculo CPU-bound

El archivo:

```text
src/cpu_bound.py
```

contiene la función:

```python
def suma_de_cuadrados(limite: int) -> int:
    ...
```

Esta función realiza cálculos intensivos y se ejecuta de dos formas:

- Secuencialmente.
- Mediante `ProcessPoolExecutor`.

### Ejecución secuencial

```python
resultados = [
    suma_de_cuadrados(limite)
    for limite in limites
]
```

### Ejecución con procesos

```python
with ProcessPoolExecutor() as executor:
    resultados = list(
        executor.map(suma_de_cuadrados, limites)
    )
```

Ambas versiones deben devolver los mismos resultados.

## ProcessPoolExecutor

`ProcessPoolExecutor` distribuye funciones entre procesos independientes.

Ventajas:

- Puede utilizar varios núcleos.
- Evita la limitación del GIL entre procesos.
- Es adecuado para tareas CPU-bound.

Costes:

- Crear procesos.
- Serializar argumentos.
- Transferir resultados.
- Gestionar memoria independiente.

En el laboratorio, el cálculo secuencial fue aproximadamente `0.04` segundos más rápido que la versión con procesos. Esto se debe a que el cálculo no era suficientemente grande para compensar el coste de crear y administrar los procesos.

## Medición y perfilado

### `perf_counter`

Se utiliza para medir bloques de código:

```python
inicio = perf_counter()
resultado = ejecutar()
duracion = perf_counter() - inicio
```

### `cProfile`

Permite observar qué funciones consumen más tiempo:

```bash
poetry run python -m cProfile -s cumulative src/main.py
```

La salida contiene información como:

- Número de llamadas.
- Tiempo propio.
- Tiempo acumulado.
- Tiempo promedio.
- Nombre y ubicación de la función.

Los tiempos acumulados incluyen el tiempo de las funciones llamadas internamente.

## Ejecución

Desde la raíz del módulo:

```bash
poetry run python -m src.main
```

El programa muestra:

- Tiempo síncrono del fetcher.
- Tiempo asíncrono del fetcher.
- Resultados de las solicitudes.
- Tiempo secuencial del cálculo.
- Tiempo con procesos.
- Comparación de resultados.

## Resultado del laboratorio

Se implementaron:

- Un fetcher HTTP síncrono.
- Un fetcher HTTP asíncrono.
- Concurrencia limitada mediante `asyncio.Semaphore`.
- Comparación de tiempos para operaciones I/O-bound.
- Un cálculo CPU-bound.
- Ejecución secuencial y con `ProcessPoolExecutor`.
- Mediciones con `perf_counter`.
- Perfilado con `cProfile`.

La comparación mostró que la concurrencia asíncrona puede mejorar el tiempo de operaciones de red, mientras que los procesos no siempre mejoran cálculos pequeños debido a su coste de administración.