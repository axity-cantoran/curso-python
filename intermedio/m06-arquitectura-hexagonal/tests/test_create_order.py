import pytest

from src.application.dto import CreateOrderRequest
from src.application.use_cases import CreateOrder
from src.domain.entities import Order
from src.infrastructure.memory_notifier import (
    InMemoryOrderNotifier,
)
from src.infrastructure.memory_repository import (
    InMemoryOrderRepository,
)


def test_order_calculates_total() -> None:
    order = Order(
        order_id=1,
        product="Teclado",
        quantity=2,
        unit_price=50.0,
    )

    assert order.total == 100.0


def test_create_order_use_case() -> None:
    repository = InMemoryOrderRepository()
    notifier = InMemoryOrderNotifier()
    use_case = CreateOrder(repository, notifier)

    result = use_case.execute(
        CreateOrderRequest(
            product="Teclado",
            quantity=2,
            unit_price=50.0,
        )
    )

    assert result.order_id == 1
    assert result.total == 100.0
    assert repository.get(1) is not None
    assert notifier.notifications[0].order_id == 1


@pytest.mark.parametrize(
    "repository_factory",
    [
        InMemoryOrderRepository,
    ],
)
def test_repository_contract(
    repository_factory: type[InMemoryOrderRepository],
) -> None:
    repository = repository_factory()

    order = Order(
        order_id=1,
        product="Teclado",
        quantity=2,
        unit_price=50.0,
    )

    repository.save(order)

    assert repository.get(1) == order
    assert repository.get(999) is None
