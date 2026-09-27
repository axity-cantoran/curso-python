from src.application.dto import (
    CreateOrderRequest,
    OrderResponse,
)
from src.application.ports import (
    EventPublisher,
    UnitOfWork,
)
from src.domain.entities import Order
from src.domain.events import OrderCreated


class CreateOrder:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        event_publisher: EventPublisher,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._event_publisher = event_publisher

    def execute(
        self,
        request: CreateOrderRequest,
    ) -> OrderResponse:
        order = Order(
            order_id=request.order_id,
            product=request.product,
            quantity=request.quantity,
            unit_price=request.unit_price,
        )

        try:
            self._unit_of_work.orders.save(order)

            event = OrderCreated(
                order_id=order.order_id,
                product=order.product,
                total=order.total,
            )

            self._unit_of_work.events.append(event)
            self._unit_of_work.commit()

        except Exception:
            self._unit_of_work.rollback()
            raise

        for event in self._unit_of_work.events:
            self._event_publisher.publish(event)

        self._unit_of_work.events.clear()

        return OrderResponse(
            order_id=order.order_id,
            product=order.product,
            quantity=order.quantity,
            unit_price=order.unit_price,
            total=order.total,
        )
