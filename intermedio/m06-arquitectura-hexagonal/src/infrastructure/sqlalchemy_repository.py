from __future__ import annotations

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base  # type: ignore[attr-defined]

from src.domain.entities import Order

Base = declarative_base()


class OrderModel(Base):  # type: ignore[misc, valid-type]
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)  # type: ignore
    product = Column(String(100), nullable=False)  # type: ignore
    quantity = Column(Integer, nullable=False)  # type: ignore
    unit_price = Column(Float, nullable=False)  # type: ignore


class SqlAlchemyOrderRepository:
    def __init__(
        self,
        database_url: str = "sqlite:///:memory:",
    ) -> None:
        self.engine = create_engine(database_url)
        self.session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)  # type: ignore

    def save(self, order: Order) -> None:
        with self.session_factory() as session:
            model = OrderModel(
                order_id=order.order_id,
                product=order.product,
                quantity=order.quantity,
                unit_price=order.unit_price,
            )
            session.merge(model)
            session.commit()

    def get(self, order_id: int) -> Order | None:
        with self.session_factory() as session:
            model = session.get(OrderModel, order_id)

            if model is None:
                return None

            return Order(
                order_id=model.order_id,
                product=model.product,
                quantity=model.quantity,
                unit_price=model.unit_price,
            )
