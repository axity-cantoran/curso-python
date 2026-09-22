import logging
from typing import TypedDict

logger = logging.getLogger(__name__)


class Metricas(TypedDict):
    cantidad_ventas: int
    unidades_vendidas: int
    ingreso_total: float
    producto_mayor_ingreso: str | None


def calcular_metricas(ventas: list[dict[str, object]]) -> Metricas:
    cantidad_ventas = len(ventas)
    unidades_vendidas = 0
    ingreso_total = 0.0
    ingresos_por_producto: dict[str, float] = {}

    for venta in ventas:
        producto = venta["producto"]
        cantidad = venta["cantidad"]
        precio = venta["precio"]

        if not isinstance(producto, str):
            logger.warning("Producto inválido: %s", producto)
            continue

        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            logger.warning("Cantidad inválida: %s", cantidad)
            continue

        if not isinstance(precio, (int, float)) or isinstance(precio, bool):
            logger.warning("Precio inválido: %s", precio)
            continue

        ingreso = cantidad * precio
        unidades_vendidas += cantidad
        ingreso_total += ingreso
        ingresos_por_producto[producto] = (
            ingresos_por_producto.get(producto, 0.0) + ingreso
        )

    producto_mayor_ingreso = (
        max(
            ingresos_por_producto,
            key=lambda producto: ingresos_por_producto[producto],
        )
        if ingresos_por_producto
        else None
    )

    logger.info("Métricas calculadas para %s ventas", cantidad_ventas)

    return {
        "cantidad_ventas": cantidad_ventas,
        "unidades_vendidas": unidades_vendidas,
        "ingreso_total": ingreso_total,
        "producto_mayor_ingreso": producto_mayor_ingreso,
    }


if __name__ == "__main__":
    from pathlib import Path

    from ingesta import leer_ventas

    ruta = Path(__file__).parent.parent / "datos" / "ventas.csv"
    ventas = leer_ventas(ruta)
    metricas = calcular_metricas(ventas)

    print(metricas)
