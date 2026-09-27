import pytest

from src.domain.entities import Order


def test_order_calculates_total() -> None:
    order = Order(
        order_id=1,
        product="Teclado",
        quantity=2,
        unit_price=50.0,
    )

    assert order.total == 100.0


@pytest.mark.parametrize(
    ("quantity", "unit_price"),
    [
        (0, 50.0),
        (2, 0.0),
        (-1, 50.0),
        (2, -10.0),
    ],
)
def test_order_rejects_invalid_values(
    quantity: int,
    unit_price: float,
) -> None:
    with pytest.raises(ValueError):
        Order(
            order_id=1,
            product="Teclado",
            quantity=quantity,
            unit_price=unit_price,
        )
