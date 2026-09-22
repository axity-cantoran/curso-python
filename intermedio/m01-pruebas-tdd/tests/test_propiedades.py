from hypothesis import given
from hypothesis import strategies as st

from src.ventas import Venta, generar_resumen


@given(
    st.lists(
        st.fixed_dictionaries(
            {
                "producto": st.just("Producto"),
                "cantidad": st.integers(min_value=1, max_value=100),
                "precio": st.floats(
                    min_value=0.01,
                    max_value=1000.0,
                    allow_nan=False,
                    allow_infinity=False,
                ),
            }
        )
    )
)
def test_resumen_propiedad_cantidad_e_ingreso(
    ventas: list[Venta],
) -> None:
    resultado = generar_resumen(ventas)

    assert resultado["cantidad_ventas"] == len(ventas)
    assert resultado["ingreso_total"] >= 0
