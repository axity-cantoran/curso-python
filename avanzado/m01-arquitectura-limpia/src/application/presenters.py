from src.application.dto import OrderResponse


class OrderPresenter:
    def present(self, response: OrderResponse) -> dict[str, object]:
        return {
            "id": response.order_id,
            "product": response.product,
            "quantity": response.quantity,
            "unit_price": response.unit_price,
            "total": response.total,
        }
