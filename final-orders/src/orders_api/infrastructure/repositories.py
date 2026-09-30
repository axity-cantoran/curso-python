import json
from collections.abc import Sequence
from datetime import UTC
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from orders_api.domain.catalog import get_product
from orders_api.domain.entities import Order, OrderItem
from orders_api.domain.enums import OrderStatus
from orders_api.infrastructure.models import OrderModel


class SqlAlchemyOrderRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, order: Order) -> Order:
        model = self._to_model(order)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)

    def get_by_id(self, order_id: UUID) -> Order | None:
        model = self._session.get(OrderModel, str(order_id))

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> Sequence[Order]:
        models = self._session.scalars(
            select(OrderModel).order_by(OrderModel.created_at)
        ).all()

        return [self._to_domain(model) for model in models]

    def update(self, order: Order) -> Order:
        model = self._session.get(OrderModel, str(order.id))

        if model is None:
            raise LookupError(f"Orden no encontrada: {order.id}")

        model.status = order.status.value
        self._session.commit()
        self._session.refresh(model)
        return self._to_domain(model)

    def delete(self, order_id: UUID) -> None:
        model = self._session.get(OrderModel, str(order_id))

        if model is None:
            raise LookupError(f"Orden no encontrada: {order_id}")

        self._session.delete(model)
        self._session.commit()

    @staticmethod
    def _to_model(order: Order) -> OrderModel:
        items = [
            {
                "product_id": item.product.id,
                "quantity": item.quantity,
            }
            for item in order.items
        ]

        return OrderModel(
            id=str(order.id),
            status=order.status.value,
            created_at=order.created_at,
            items_json=json.dumps(items),
        )

    @staticmethod
    def _to_domain(model: OrderModel) -> Order:
        raw_items = json.loads(model.items_json)
        items = [
            OrderItem(
                product=get_product(item["product_id"]),
                quantity=item["quantity"],
            )
            for item in raw_items
        ]

        created_at = model.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)

        return Order(
            id=UUID(model.id),
            items=items,
            status=OrderStatus(model.status),
            created_at=created_at,
        )
