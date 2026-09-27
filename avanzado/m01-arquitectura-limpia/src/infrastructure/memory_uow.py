from src.application.ports import OrderRepository
from src.domain.entities import Order
from src.domain.events import OrderCreated


class MemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self.orders: dict[int, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.order_id] = order

    def get(self, order_id: int) -> Order | None:
        return self.orders.get(order_id)


class MemoryUnitOfWork:
    orders: OrderRepository
    events: list[OrderCreated]
    committed: bool
    rolled_back: bool

    def __init__(self) -> None:
        self.orders = MemoryOrderRepository()
        self.events = []
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True
