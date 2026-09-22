from typing import Protocol, TypedDict


class Venta(TypedDict):
    producto: str
    cantidad: int
    precio: float


class Resumen(TypedDict):
    cantidad_ventas: int
    ingreso_total: float


class FuenteVentas(Protocol):
    def obtener_ventas(self) -> list[Venta]: ...


def generar_resumen(ventas: list[Venta]) -> Resumen:
    ingreso_total = 0.0

    for venta in ventas:
        cantidad = venta["cantidad"]
        precio = venta["precio"]

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero")

        ingreso_total += cantidad * precio

    return {
        "cantidad_ventas": len(ventas),
        "ingreso_total": ingreso_total,
    }


def obtener_ventas_desde_fuente(
    fuente: FuenteVentas,
) -> list[Venta]:
    return fuente.obtener_ventas()
