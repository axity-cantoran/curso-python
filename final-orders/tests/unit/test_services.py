from collections.abc import Sequence
from uuid import UUID

import pytest

from orders_api.application.schemas import (
    ChangeOrderStatusCommand,
    CreateOrderCommand,
)
from orders_api.application.services import OrderService
from orders_api.domain.entities import Order
from orders_api.domain.enums import OrderStatus
from orders_api.domain.errors import InvalidOrderStatusError


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[UUID, Order] = {}

    def add(self, order: Order) -> Order:
        self.orders[order.id] = order
        return order

    def get_by_id(self, order_id: UUID) -> Order | None:
        return self.orders.get(order_id)

    def list_all(self) -> Sequence[Order]:
        return list(self.orders.values())

    def update(self, order: Order) -> Order:
        self.orders[order.id] = order
        return order

    def delete(self, order_id: UUID) -> None:
        del self.orders[order_id]


def test_service_creates_order() -> None:
    repository = InMemoryOrderRepository()
    service = OrderService(repository)

    order = service.create_order(CreateOrderCommand(products=[("caballero", 1)]))

    assert order.status is OrderStatus.PENDING
    assert repository.get_by_id(order.id) is order


def test_service_changes_order_status() -> None:
    repository = InMemoryOrderRepository()
    service = OrderService(repository)

    order = service.create_order(CreateOrderCommand(products=[("robot", 2)]))

    updated = service.change_status(
        ChangeOrderStatusCommand(
            order_id=order.id,
            status=OrderStatus.CONFIRMED,
        )
    )

    assert updated.status is OrderStatus.CONFIRMED


def test_service_lists_orders() -> None:
    repository = InMemoryOrderRepository()
    service = OrderService(repository)

    service.create_order(CreateOrderCommand(products=[("alienigena", 1)]))

    assert len(service.list_orders()) == 1


def test_service_deletes_pending_order() -> None:
    repository = InMemoryOrderRepository()
    service = OrderService(repository)

    order = service.create_order(CreateOrderCommand(products=[("accesorios", 1)]))

    service.delete_order(order.id)

    assert repository.get_by_id(order.id) is None


def test_service_rejects_deleting_confirmed_order() -> None:
    repository = InMemoryOrderRepository()
    service = OrderService(repository)

    order = service.create_order(CreateOrderCommand(products=[("herramientas", 1)]))
    service.change_status(
        ChangeOrderStatusCommand(
            order_id=order.id,
            status=OrderStatus.CONFIRMED,
        )
    )

    with pytest.raises(InvalidOrderStatusError):
        service.delete_order(order.id)
