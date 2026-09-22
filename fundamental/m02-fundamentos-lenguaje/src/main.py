import json
import re
from pathlib import Path

# Construcción de la ruta al archivo JSON de usuarios
# donde __file___ es la ruta del archivo actual (main.py)
# parent.parent sube dos niveles en el árbol de directorios,
# y luego se agrega la carpeta "datos" y el archivo "usuarios.json".
RUTA_DATOS = Path(__file__).parent.parent / "datos" / "usuarios.json"
PATRON_CORREO = r"^[\w.-]+@[\w.-]+\.\w+$"


# Función para cargar los usuarios desde el archivo JSON
def cargar_usuarios(ruta):
    try:
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"No se encontró el archivo de usuarios: {ruta}"
        ) from error
    except json.JSONDecodeError as error:
        raise ValueError(f"El archivo no contiene un JSON válido: {ruta}") from error

    if not isinstance(datos, list):
        raise TypeError("El JSON debe contener una lista de usuarios")

    return datos


def correo_es_valido(correo):
    return re.fullmatch(PATRON_CORREO, correo) is not None


def filtrar_usuarios(usuarios):
    usuarios_validos = []

    for usuario in usuarios:
        if not isinstance(usuario, dict):
            continue

        if usuario.get("activo") is not True:
            continue

        correo = usuario.get("correo")

        if not isinstance(correo, str):
            continue

        if not correo_es_valido(correo):
            continue

        usuarios_validos.append(usuario)

    return usuarios_validos


def contar_por_rol(usuarios):
    resumen = {}

    for usuario in usuarios:
        rol = usuario.get("rol", "sin_rol")
        resumen[rol] = resumen.get(rol, 0) + 1

    return resumen


def main():
    try:
        usuarios = cargar_usuarios(RUTA_DATOS)
    except (FileNotFoundError, ValueError, TypeError) as error:
        print(f"Error: {error}")
        return

    usuarios_validos = filtrar_usuarios(usuarios)
    resumen_por_rol = contar_por_rol(usuarios_validos)

    print("Usuarios activos con correo válido:")

    for usuario in usuarios_validos:
        print(f"- {usuario['nombre']}: {usuario['correo']}")

    print("\nResumen por rol:")

    for rol, cantidad in resumen_por_rol.items():
        print(f"- {rol}: {cantidad}")


if __name__ == "__main__":
    main()
