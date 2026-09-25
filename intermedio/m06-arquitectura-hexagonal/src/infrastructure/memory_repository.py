from src.domain.entities import Order


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[int, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.order_id] = order

    def get(self, order_id: int) -> Order | None:
        return self.orders.get(order_id)
