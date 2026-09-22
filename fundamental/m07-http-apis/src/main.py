import logging
from pathlib import Path

from cliente_http import crear_cliente
from descarga import descargar_stream


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main() -> None:
    configurar_logging()

    url = "http://localhost:8080/archivo.bin"
    destino = Path("descargas") / "archivo.bin"

    try:
        with crear_cliente() as cliente:
            descargar_stream(cliente, url, destino)
    except Exception:
        logging.getLogger(__name__).exception("La descarga no pudo completarse")
        return

    print(f"Archivo descargado en: {destino}")


if __name__ == "__main__":
    main()
