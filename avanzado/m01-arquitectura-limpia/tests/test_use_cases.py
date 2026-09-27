from src.application.dto import CreateOrderRequest
from src.application.use_cases import CreateOrder
from src.infrastructure.memory_notifier import (
    InMemoryOrderNotifier,
)
from src.infrastructure.memory_uow import MemoryUnitOfWork


def test_create_order_commits_and_publishes_event() -> None:
    unit_of_work = MemoryUnitOfWork()
    notifier = InMemoryOrderNotifier()
    use_case = CreateOrder(unit_of_work, notifier)

    result = use_case.execute(
        CreateOrderRequest(
            order_id=1,
            product="Teclado",
            quantity=2,
            unit_price=50.0,
        )
    )

    assert result.total == 100.0
    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False
    assert len(notifier.events) == 1
    assert notifier.events[0].order_id == 1


class FailingUnitOfWork(MemoryUnitOfWork):
    def commit(self) -> None:
        raise RuntimeError("Error de persistencia")


def test_create_order_rolls_back_on_failure() -> None:
    unit_of_work = FailingUnitOfWork()
    notifier = InMemoryOrderNotifier()
    use_case = CreateOrder(unit_of_work, notifier)

    request = CreateOrderRequest(
        order_id=1,
        product="Teclado",
        quantity=2,
        unit_price=50.0,
    )

    try:
        use_case.execute(request)
    except RuntimeError:
        pass

    assert unit_of_work.rolled_back is True
    assert notifier.events == []
