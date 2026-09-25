from src.domain import Order
from src.ports import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def create_order(
        self,
        order: Order,
    ) -> Order:
        if order.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

        if order.unit_price <= 0:
            raise ValueError("El precio debe ser mayor que cero")

        self._repository.save(order)
        return order

    def get_order(self, order_id: int) -> Order | None:
        return self._repository.get(order_id)
