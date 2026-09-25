from dataclasses import dataclass


@dataclass(frozen=True)
class CreateOrderRequest:
    product: str
    quantity: int
    unit_price: float


@dataclass(frozen=True)
class OrderResponse:
    order_id: int
    product: str
    quantity: int
    unit_price: float
    total: float
