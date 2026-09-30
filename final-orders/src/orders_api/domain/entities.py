from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from orders_api.domain.catalog import Product, get_product
from orders_api.domain.enums import OrderStatus
from orders_api.domain.errors import (
    InvalidOrderStatusError,
    InvalidQuantityError,
    ProductNotFoundError,
)


@dataclass(slots=True)
class OrderItem:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise InvalidQuantityError("La cantidad debe ser mayor que cero.")


@dataclass(slots=True)
class Order:
    items: list[OrderItem]
    id: UUID = field(default_factory=uuid4)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def confirm(self) -> None:
        if self.status is not OrderStatus.PENDING:
            raise InvalidOrderStatusError("Solo una orden pendiente puede confirmarse.")
        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:
        if self.status is not OrderStatus.PENDING:
            raise InvalidOrderStatusError("Solo una orden pendiente puede cancelarse.")
        self.status = OrderStatus.CANCELLED

    @classmethod
    def create(
        cls,
        products: list[tuple[str, int]],
    ) -> "Order":
        items: list[OrderItem] = []

        for product_id, quantity in products:
            try:
                product = get_product(product_id)
            except ValueError as error:
                raise ProductNotFoundError(str(error)) from error

            items.append(OrderItem(product=product, quantity=quantity))

        if not items:
            raise InvalidQuantityError("La orden debe contener al menos un producto.")

        return cls(items=items)
