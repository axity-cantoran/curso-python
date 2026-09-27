from src.application.dto import CreateOrderRequest
from src.application.presenters import OrderPresenter
from src.application.use_cases import CreateOrder
from src.controllers.orders import OrderController
from src.infrastructure.memory_notifier import (
    InMemoryOrderNotifier,
)
from src.infrastructure.memory_uow import MemoryUnitOfWork


def create_order_controller() -> OrderController:
    unit_of_work = MemoryUnitOfWork()
    notifier = InMemoryOrderNotifier()
    use_case = CreateOrder(unit_of_work, notifier)
    presenter = OrderPresenter()

    return OrderController(use_case, presenter)


def create_order_request() -> CreateOrderRequest:
    return CreateOrderRequest(
        order_id=1,
        product="Teclado",
        quantity=2,
        unit_price=50.0,
    )
