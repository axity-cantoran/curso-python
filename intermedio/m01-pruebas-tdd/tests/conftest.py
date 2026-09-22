import pytest

from src.ventas import Venta


@pytest.fixture
def ventas_validas() -> list[Venta]:
    return [
        {
            "producto": "Teclado",
            "cantidad": 2,
            "precio": 50.0,
        },
        {
            "producto": "Monitor",
            "cantidad": 1,
            "precio": 200.0,
        },
    ]
