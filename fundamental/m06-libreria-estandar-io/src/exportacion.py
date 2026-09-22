import json
import logging
from pathlib import Path

from metricas import Metricas

logger = logging.getLogger(__name__)


def exportar_metricas(metricas: Metricas, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)

    try:
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(metricas, archivo, ensure_ascii=False, indent=2)
    except OSError:
        logger.exception("No se pudieron exportar las métricas a %s", ruta)
        raise

    logger.info("Métricas exportadas a %s", ruta)


if __name__ == "__main__":
    metricas: Metricas = {
        "cantidad_ventas": 5,
        "unidades_vendidas": 9,
        "ingreso_total": 825.0,
        "producto_mayor_ingreso": "Monitor",
    }

    ruta = Path(__file__).parent.parent / "salidas" / "metricas.json"
    exportar_metricas(metricas, ruta)
