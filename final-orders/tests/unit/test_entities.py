import pytest

from orders_api.domain.entities import Order
from orders_api.domain.enums import OrderStatus
from orders_api.domain.errors import (
    InvalidOrderStatusError,
    InvalidQuantityError,
    ProductNotFoundError,
)


def test_creates_pending_order_with_catalog_products() -> None:
    order = Order.create(
        [
            ("caballero", 1),
            ("accesorios", 2),
        ]
    )

    assert order.status is OrderStatus.PENDING
    assert len(order.items) == 2
    assert order.items[0].product.name == "Caballero"


def test_confirms_pending_order() -> None:
    order = Order.create([("mago", 1)])

    order.confirm()

    assert order.status is OrderStatus.CONFIRMED


def test_cancels_pending_order() -> None:
    order = Order.create([("robot", 1)])

    order.cancel()

    assert order.status is OrderStatus.CANCELLED


def test_rejects_invalid_status_transition() -> None:
    order = Order.create([("alienigena", 1)])
    order.confirm()

    with pytest.raises(InvalidOrderStatusError):
        order.cancel()


def test_rejects_unknown_product() -> None:
    with pytest.raises(ProductNotFoundError):
        Order.create([("unknown", 1)])


def test_rejects_non_positive_quantity() -> None:
    with pytest.raises(InvalidQuantityError):
        Order.create([("herramientas", 0)])
