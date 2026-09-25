from typing import Protocol

from src.domain import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...

    def get(self, order_id: int) -> Order | None: ...
