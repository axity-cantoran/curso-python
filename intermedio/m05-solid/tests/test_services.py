import sqlite3

import pytest

from src.domain import Order
from src.providers import create_repository
from src.services import OrderService


@pytest.mark.parametrize("kind", ["memory", "sql"])
def test_service_works_with_both_repositories(
    kind: str,
) -> None:
    connection = sqlite3.connect(":memory:")

    try:
        repository = create_repository(
            kind,
            connection if kind == "sql" else None,
        )
        service = OrderService(repository)

        order = Order(
            order_id=1,
            product="Teclado",
            quantity=2,
            unit_price=50.0,
        )

        created = service.create_order(order)
        stored = service.get_order(1)

        assert created == order
        assert stored == order
    finally:
        connection.close()


def test_service_rejects_invalid_quantity() -> None:
    service = OrderService(create_repository("memory"))

    order = Order(
        order_id=1,
        product="Teclado",
        quantity=0,
        unit_price=50.0,
    )

    with pytest.raises(ValueError, match="cantidad"):
        service.create_order(order)


def test_service_rejects_invalid_price() -> None:
    service = OrderService(create_repository("memory"))

    order = Order(
        order_id=1,
        product="Teclado",
        quantity=2,
        unit_price=0.0,
    )

    with pytest.raises(ValueError, match="precio"):
        service.create_order(order)
