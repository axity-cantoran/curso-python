from typing import Protocol

from src.domain.entities import Order
from src.domain.events import OrderCreated


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...

    def get(self, order_id: int) -> Order | None: ...


class UnitOfWork(Protocol):
    orders: OrderRepository
    events: list[OrderCreated]

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


class EventPublisher(Protocol):
    def publish(self, event: OrderCreated) -> None: ...
