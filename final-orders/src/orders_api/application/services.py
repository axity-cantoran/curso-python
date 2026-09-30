from collections.abc import Sequence
from uuid import UUID

from orders_api.application.ports import OrderRepository
from orders_api.application.schemas import (
    ChangeOrderStatusCommand,
    CreateOrderCommand,
)
from orders_api.domain.entities import Order
from orders_api.domain.enums import OrderStatus
from orders_api.domain.errors import InvalidOrderStatusError


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def create_order(self, command: CreateOrderCommand) -> Order:
        order = Order.create(command.products)
        return self._repository.add(order)

    def get_order(self, order_id: UUID) -> Order:
        order = self._repository.get_by_id(order_id)

        if order is None:
            raise LookupError(f"Orden no encontrada: {order_id}")

        return order

    def list_orders(self) -> Sequence[Order]:
        return self._repository.list_all()

    def change_status(self, command: ChangeOrderStatusCommand) -> Order:
        order = self.get_order(command.order_id)

        if command.status is OrderStatus.CONFIRMED:
            order.confirm()
        elif command.status is OrderStatus.CANCELLED:
            order.cancel()
        else:
            raise InvalidOrderStatusError(
                "No se puede cambiar manualmente al estado pendiente."
            )

        return self._repository.update(order)

    def delete_order(self, order_id: UUID) -> None:
        order = self.get_order(order_id)

        if order.status is not OrderStatus.PENDING:
            raise InvalidOrderStatusError("Solo se pueden eliminar órdenes pendientes.")

        self._repository.delete(order_id)
