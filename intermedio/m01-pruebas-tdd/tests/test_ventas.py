from unittest.mock import Mock

import pytest

from src.ventas import Venta, generar_resumen, obtener_ventas_desde_fuente


def test_generar_resumen_sin_ventas() -> None:
    resultado = generar_resumen([])

    assert resultado == {
        "cantidad_ventas": 0,
        "ingreso_total": 0.0,
    }


def test_generar_resumen_con_ventas() -> None:
    ventas: list[Venta] = [
        {"producto": "Teclado", "cantidad": 2, "precio": 50.0},
        {"producto": "Monitor", "cantidad": 1, "precio": 200.0},
    ]

    resultado = generar_resumen(ventas)

    assert resultado == {
        "cantidad_ventas": 2,
        "ingreso_total": 300.0,
    }


@pytest.mark.parametrize(
    "venta_invalida",
    [
        {"producto": "Teclado", "cantidad": 0, "precio": 50.0},
        {"producto": "Teclado", "cantidad": -1, "precio": 50.0},
        {"producto": "Teclado", "cantidad": 2, "precio": 0.0},
        {"producto": "Teclado", "cantidad": 2, "precio": -10.0},
    ],
)
def test_generar_resumen_rechaza_ventas_invalidas(
    venta_invalida: Venta,
) -> None:
    with pytest.raises(ValueError):
        generar_resumen([venta_invalida])


@pytest.mark.unit
def test_generar_resumen_con_fixture(
    ventas_validas: list[Venta],
) -> None:
    resultado = generar_resumen(ventas_validas)

    assert resultado == {
        "cantidad_ventas": 2,
        "ingreso_total": 300.0,
    }


def test_obtener_ventas_desde_fuente() -> None:
    fuente = Mock()
    fuente.obtener_ventas.return_value = [
        {"producto": "Teclado", "cantidad": 2, "precio": 50.0},
    ]

    resultado = obtener_ventas_desde_fuente(fuente)

    assert resultado == [
        {"producto": "Teclado", "cantidad": 2, "precio": 50.0},
    ]
    fuente.obtener_ventas.assert_called_once_with()


def test_obtener_ventas_desde_fuente_falla() -> None:
    fuente = Mock()
    fuente.obtener_ventas.side_effect = ConnectionError("Fuente no disponible")

    with pytest.raises(ConnectionError, match="Fuente no disponible"):
        obtener_ventas_desde_fuente(fuente)

    fuente.obtener_ventas.assert_called_once_with()
