from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from orders_api.domain.enums import OrderStatus


class OrderItemRequest(BaseModel):
    product_id: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class CreateOrderRequest(BaseModel):
    items: list[OrderItemRequest] = Field(min_length=1)


class ChangeOrderStatusRequest(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int


class OrderResponse(BaseModel):
    id: UUID
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemResponse]


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
