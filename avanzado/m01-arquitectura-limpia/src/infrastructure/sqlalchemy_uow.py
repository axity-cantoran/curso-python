from sqlalchemy import (  # type: ignore[import-untyped]
    Column,
    Float,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import sessionmaker  # type: ignore[import-untyped]
from sqlalchemy.orm import declarative_base  # type: ignore[attr-defined, import-untyped]

from src.domain.entities import Order

# SQLAlchemy 1.4.54 genera constructores, metadata y atributos ORM
# dinámicamente. Pylance puede mostrar advertencias sobre estos elementos;
# mypy y las pruebas de ejecución validan el comportamiento real.


Base = declarative_base()


class OrderModel(Base):  # type: ignore[misc, valid-type]
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    product = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)


class SqlAlchemyOrderRepository:
    def __init__(self, session):
        self.session = session

    def save(self, order: Order) -> None:
        model = OrderModel(
            order_id=order.order_id,
            product=order.product,
            quantity=order.quantity,
            unit_price=order.unit_price,
        )
        self.session.merge(model)

    def get(self, order_id: int) -> Order | None:
        model = self.session.get(OrderModel, order_id)

        if model is None:
            return None

        return Order(
            order_id=model.order_id,
            product=model.product,
            quantity=model.quantity,
            unit_price=model.unit_price,
        )


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        database_url: str = "sqlite:///:memory:",
    ) -> None:
        self.engine = create_engine(database_url)
        self.session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.session = self.session_factory()
        self.orders = SqlAlchemyOrderRepository(self.session)
        self.events: list[object] = []

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
