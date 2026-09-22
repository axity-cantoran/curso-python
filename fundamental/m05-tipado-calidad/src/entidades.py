from dataclasses import dataclass, field
from typing import Any


@dataclass
class Order:
    order_id: str
    product: str
    unit_price: float
    quantity: int
    tax_rate: float = 0.16
    subtotal: float = field(init=False)
    tax: float = field(init=False)
    total: float = field(init=False)

    def __post_init__(self) -> None:
        self.subtotal = self.unit_price * self.quantity
        self.tax = self.subtotal * self.tax_rate
        self.total = self.subtotal + self.tax

    def __str__(self) -> str:
        return f"Order {self.order_id}: {self.product} - Total: {self.total:.2f}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Order):
            return NotImplemented

        return self.order_id == other.order_id

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Order):
            return NotImplemented

        return self.total < other.total
