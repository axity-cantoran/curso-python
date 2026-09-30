from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from orders_api.domain.entities import Order
from orders_api.domain.enums import OrderStatus
from orders_api.infrastructure.database import Base
from orders_api.infrastructure.repositories import SqlAlchemyOrderRepository


def test_repository_persists_order() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = SqlAlchemyOrderRepository(session)
        order = Order.create(
            [
                ("caballero", 1),
                ("herramientas", 2),
            ]
        )

        repository.add(order)
        stored = repository.get_by_id(order.id)

        assert stored is not None
        assert stored.id == order.id
        assert stored.status is OrderStatus.PENDING
        assert len(stored.items) == 2


def test_repository_deletes_order() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = SqlAlchemyOrderRepository(session)
        order = Order.create([("mago", 1)])

        repository.add(order)
        repository.delete(order.id)

        assert repository.get_by_id(order.id) is None
