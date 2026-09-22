import csv
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def leer_ventas(ruta: Path) -> list[dict[str, object]]:
    ventas: list[dict[str, object]] = []

    logger.info("Iniciando lectura del archivo: %s", ruta)

    try:
        with ruta.open(newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    venta = {
                        "fecha": datetime.fromisoformat(fila["fecha"]),
                        "producto": fila["producto"],
                        "cantidad": int(fila["cantidad"]),
                        "precio": float(fila["precio"]),
                    }
                except (TypeError, ValueError, KeyError) as error:
                    logger.warning(
                        "Fila %s descartada por datos inválidos: %s",
                        numero_fila,
                        error,
                    )
                    continue

                ventas.append(venta)
                logger.debug("Fila %s procesada: %s", numero_fila, venta)

    except FileNotFoundError:
        logger.error("No se encontró el archivo: %s", ruta)
        raise

    logger.info("Lectura finalizada. Ventas válidas: %s", len(ventas))

    return ventas


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    ruta = Path(__file__).parent.parent / "datos" / "ventas.csv"
    ventas = leer_ventas(ruta)

    for venta in ventas:
        print(venta)
