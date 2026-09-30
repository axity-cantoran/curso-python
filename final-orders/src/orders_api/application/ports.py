from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from orders_api.domain.entities import Order


class OrderRepository(Protocol):
    def add(self, order: Order) -> Order: ...

    def get_by_id(self, order_id: UUID) -> Order | None: ...

    def list_all(self) -> Sequence[Order]: ...

    def update(self, order: Order) -> Order: ...

    def delete(self, order_id: UUID) -> None: ...
