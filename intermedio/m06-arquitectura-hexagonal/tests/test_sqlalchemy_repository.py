from src.domain.entities import Order
from src.infrastructure.sqlalchemy_repository import (
    SqlAlchemyOrderRepository,
)


def test_sqlalchemy_repository_contract() -> None:
    repository = SqlAlchemyOrderRepository()

    order = Order(
        order_id=1,
        product="Monitor",
        quantity=1,
        unit_price=200.0,
    )

    repository.save(order)

    assert repository.get(1) == order
    assert repository.get(999) is None
