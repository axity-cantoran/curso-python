from dataclasses import dataclass
from uuid import UUID

from orders_api.domain.enums import OrderStatus


@dataclass(frozen=True, slots=True)
class CreateOrderCommand:
    products: list[tuple[str, int]]


@dataclass(frozen=True, slots=True)
class ChangeOrderStatusCommand:
    order_id: UUID
    status: OrderStatus
