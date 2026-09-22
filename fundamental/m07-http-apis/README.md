# Módulo 07: HTTP y consumo de APIs

## Descripción

Este módulo implementa un cliente HTTP robusto con `httpx`, capaz de gestionar timeouts, reintentos, errores HTTP y descargas por streaming.

Las pruebas se realizan contra un servidor HTTP simulado mediante Smocker, ejecutado dentro de Docker.

## Objetivos

- Construir clientes HTTP robustos.
- Configurar timeouts explícitos.
- Gestionar errores de conexión y errores HTTP temporales.
- Implementar reintentos con backoff.
- Descargar respuestas grandes sin cargar todo el contenido en memoria.
- Guardar archivos de forma segura mediante archivos temporales.

## Entorno

- Python 3.12
- Poetry
- Ambiente virtual `.venv`
- Visual Studio Code
- Git Bash
- `httpx` con soporte HTTP/2
- Smocker 0.18.5
- Docker Compose
- Black
- isort
- Ruff
- mypy
- pre-commit
- Git local

## Estructura del proyecto

```text
m07-http-apis/
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── README.md
├── smocker/
│   ├── archivo.bin
│   ├── error-stub.json
│   └── stub.json
├── src/
│   ├── cliente_http.py
│   ├── descarga.py
│   └── main.py
└── descargas/
```

La carpeta `descargas/` contiene archivos generados durante las pruebas y está excluida de Git.

## Cliente HTTP

El módulo `src/cliente_http.py` contiene la configuración principal del cliente `httpx`.

### Configuración aplicada

- Cliente síncrono mediante `httpx.Client`.
- Soporte solicitado para HTTP/2.
- Timeouts separados para conexión, lectura, escritura y pool.
- Encabezado `User-Agent`.
- Cierre automático mediante context manager.

Ejemplo conceptual:

```python
with crear_cliente() as cliente:
    ...
```

El context manager garantiza que el cliente se cierre incluso si ocurre una excepción.

## Timeouts

Se configuraron límites para:

- `connect`: tiempo máximo para establecer la conexión.
- `read`: tiempo máximo para recibir datos.
- `write`: tiempo máximo para enviar datos.
- `pool`: tiempo máximo para obtener una conexión disponible.

Estos límites evitan que una solicitud permanezca bloqueada indefinidamente.

## Manejo de respuestas HTTP

Se implementó una validación mediante:

```python
def validar_respuesta(respuesta: httpx.Response) -> httpx.Response:
    ...
```

La función:

- Acepta respuestas exitosas.
- Considera reintentables las respuestas `429`.
- Considera reintentables las respuestas `5xx`.
- Lanza errores para otras respuestas `4xx` mediante `raise_for_status()`.

Los errores temporales se representan mediante:

```python
class ErrorHTTPReintentable(Exception):
    ...
```

## Reintentos y backoff

Se implementó un decorador de reintentos con:

- Cantidad máxima de intentos.
- Tiempo de espera inicial.
- Factor de backoff.
- Captura de errores de conexión.
- Captura de timeouts.
- Captura de errores HTTP temporales.
- Relanzamiento de la última excepción.

Los tipos de error reintentables incluyen:

- `httpx.TimeoutException`.
- `httpx.ConnectError`.
- `ErrorHTTPReintentable`.

Con una espera inicial de `0.5` segundos y un factor de `2`, las esperas son aproximadamente:

```text
0.5 segundos
1.0 segundos
```

El decorador utiliza `ParamSpec` y `TypeVar` para conservar el tipado de la función decorada.

## Descarga por streaming

El módulo `src/descarga.py` implementa la descarga incremental.

La respuesta se procesa mediante:

```python
cliente.stream("GET", url)
```

y:

```python
respuesta.iter_bytes(chunk_size=...)
```

El tamaño predeterminado de bloque es:

```text
64 KiB
```

Esto permite procesar archivos grandes sin cargarlos completamente en memoria.

## Archivos temporales

Las descargas se escriben inicialmente en un archivo con extensión:

```text
.part
```

Ejemplo:

```text
archivo.bin.part
```

Cuando la descarga finaliza correctamente:

```text
archivo.bin.part → archivo.bin
```

Si ocurre una excepción:

- Se elimina el archivo temporal.
- No se deja un archivo final incompleto.
- La excepción continúa propagándose.

## Smocker

Smocker se utilizó para simular respuestas HTTP sin depender de una API externa.

Los mocks actuales representan respuestas controladas:

```text
GET /archivo.bin → 200
GET /ejemplo.bin → 200
GET /error.bin → 503
```

Los mocks permiten probar:

- Descargas exitosas.
- Errores HTTP temporales.
- Reintentos.
- Respuestas con distintos cuerpos y encabezados.

### Código de respuesta 666

Smocker utiliza el código `666` cuando no encuentra un mock que coincida con la solicitud.

Esto suele ocurrir cuando:

- La ruta no coincide.
- El método HTTP es diferente.
- El mock fue eliminado después de reiniciar o restablecer Smocker.
- El endpoint no fue registrado.

El código `666` no representa un error real del servidor de producción; es una respuesta especial del servidor simulado.

## Docker Compose

Smocker se ejecuta mediante Docker Compose.

El archivo `docker-compose.yml` fija la versión utilizada:

```yaml
services:
  smocker:
    image: thiht/smocker:0.18.5
    container_name: m07-smocker
    ports:
      - "8080:8080"
      - "8081:8081"
```

Puertos utilizados:

- `8080`: servidor HTTP simulado.
- `8081`: interfaz y API administrativa de Smocker.

### Comandos principales

Iniciar Smocker:

```bash
docker compose up -d
```

Verificar el contenedor:

```bash
docker compose ps
```

Consultar logs:

```bash
docker compose logs smocker
```

Detener temporalmente:

```bash
docker compose stop
```

Reanudar:

```bash
docker compose start
```

Restablecer los mocks:

```bash
curl -i -X POST http://localhost:8081/reset
```

Consultar los mocks registrados:

```bash
curl -s http://localhost:8081/mocks
```

## Ejecución del cliente

Desde la raíz del proyecto:

```bash
poetry run python src/main.py
```

Para la descarga exitosa, `main.py` utiliza:

```python
url = "http://localhost:8080/archivo.bin"
destino = Path("descargas") / "archivo.bin"
```

El contenido descargado puede comprobarse con:

```bash
cat descargas/archivo.bin
```

Resultado esperado:

```text
Contenido de prueba para descarga por streaming.
```

## Pruebas realizadas

### Descarga exitosa

Se comprobó que:

- Smocker responde con `200 OK`.
- `httpx` recibe la respuesta.
- La respuesta se procesa por streaming.
- El contenido se guarda en disco.
- El archivo temporal se renombra correctamente.

### Error de conexión

Se utilizó temporalmente:

```text
http://localhost:9999/archivo.bin
```

Como no había ningún servicio escuchando en ese puerto:

- Se produjo `httpx.ConnectError`.
- Se ejecutaron los reintentos.
- Se aplicó backoff progresivo.
- La excepción se relanzó después del último intento.
- No quedó un archivo final incompleto.

### Error HTTP temporal

Se configuró un mock con respuesta `503`:

```text
GET /error.bin → 503
```

La respuesta fue identificada como temporal mediante `ErrorHTTPReintentable` y activó la política de reintentos.

## Logging

El cliente registra información como:

- Inicio de la descarga.
- URL solicitada.
- Intentos fallidos.
- Tiempo de espera entre reintentos.
- Cierre del cliente.
- Finalización de la descarga.
- Errores con traceback.

Ejemplo:

```text
[INFO] Iniciando descarga desde ...
[WARNING] Descarga fallida en intento 1 ...
[ERROR] La descarga no pudo completarse
```

## Archivos excluidos de Git

El archivo `.gitignore` excluye:

```text
.venv/
__pycache__/
*.py[cod]
.ruff_cache/
.pytest_cache/
.mypy_cache/
descargas/
```

Estos archivos y carpetas se generan localmente o contienen resultados de pruebas.

## Resultado del laboratorio

Se implementó un cliente HTTP capaz de:

- Consumir un servidor simulado con Smocker.
- Utilizar `httpx` con soporte HTTP/2.
- Aplicar timeouts.
- Reintentar errores de conexión y errores HTTP temporales.
- Aplicar backoff progresivo.
- Procesar respuestas mediante streaming.
- Escribir datos incrementalmente en disco.
- Evitar archivos finales incompletos.
- Registrar eventos y errores.
- Validar el código con Black, Ruff, mypy y pre-commit.
- Ejecutarse mediante un entorno reproducible con Docker Compose.