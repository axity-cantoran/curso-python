import logging
from pathlib import Path

from exportacion import exportar_metricas
from ingesta import leer_ventas
from metricas import calcular_metricas


def configurar_logging() -> None:
    ruta_logs = Path(__file__).parent.parent / "logs" / "ventas.log"
    ruta_logs.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(ruta_logs, encoding="utf-8"),
        ],
    )


def main() -> None:
    configurar_logging()
    logger = logging.getLogger(__name__)

    raiz = Path(__file__).parent.parent
    ruta_csv = raiz / "datos" / "ventas.csv"
    ruta_json = raiz / "salidas" / "metricas.json"

    logger.info("Iniciando procesamiento de ventas")

    try:
        ventas = leer_ventas(ruta_csv)
        metricas = calcular_metricas(ventas)
        exportar_metricas(metricas, ruta_json)
    except (FileNotFoundError, OSError, ValueError) as error:
        logger.exception("El procesamiento terminó con error: %s", error)
        return

    logger.info("Procesamiento finalizado correctamente")
    print(f"Métricas exportadas a: {ruta_json}")


if __name__ == "__main__":
    main()
