from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    order_id: int
    product: str
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

        if self.unit_price <= 0:
            raise ValueError("El precio debe ser mayor que cero")

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price
