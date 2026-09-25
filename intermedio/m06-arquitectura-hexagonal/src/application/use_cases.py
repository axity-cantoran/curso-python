from src.application.dto import (
    CreateOrderRequest,
    OrderResponse,
)
from src.application.ports import (
    OrderNotifier,
    OrderRepository,
)
from src.domain.entities import Order


class CreateOrder:
    def __init__(
        self,
        repository: OrderRepository,
        notifier: OrderNotifier,
    ) -> None:
        self._repository = repository
        self._notifier = notifier

    def execute(
        self,
        request: CreateOrderRequest,
    ) -> OrderResponse:
        order = Order(
            order_id=self._next_id(),
            product=request.product,
            quantity=request.quantity,
            unit_price=request.unit_price,
        )

        self._repository.save(order)
        self._notifier.notify_order_created(order)

        return OrderResponse(
            order_id=order.order_id,
            product=order.product,
            quantity=order.quantity,
            unit_price=order.unit_price,
            total=order.total,
        )

    def _next_id(self) -> int:
        return 1
