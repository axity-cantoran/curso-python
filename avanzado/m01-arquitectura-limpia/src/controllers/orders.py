from src.application.dto import (
    CreateOrderRequest,
)
from src.application.presenters import OrderPresenter
from src.application.use_cases import CreateOrder


class OrderController:
    def __init__(
        self,
        use_case: CreateOrder,
        presenter: OrderPresenter,
    ) -> None:
        self._use_case = use_case
        self._presenter = presenter

    def handle(
        self,
        data: CreateOrderRequest,
    ) -> dict[str, object]:
        response = self._use_case.execute(data)
        return self._presenter.present(response)
