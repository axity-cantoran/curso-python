from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from orders_api.api.dependencies import get_order_service, require_api_key
from orders_api.api.schemas import (
    ChangeOrderStatusRequest,
    CreateOrderRequest,
    OrderItemResponse,
    OrderListResponse,
    OrderResponse,
)
from orders_api.application.schemas import (
    ChangeOrderStatusCommand,
    CreateOrderCommand,
)
from orders_api.application.services import OrderService
from orders_api.domain.entities import Order
from orders_api.domain.errors import DomainError

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(require_api_key)],
)


def _to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        status=order.status,
        created_at=order.created_at,
        items=[
            OrderItemResponse(
                product_id=item.product.id,
                product_name=item.product.name,
                quantity=item.quantity,
            )
            for item in order.items
        ],
    )


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    try:
        command = CreateOrderCommand(
            products=[(item.product_id, item.quantity) for item in request.items]
        )
        return _to_response(service.create_order(command))
    except DomainError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=OrderListResponse,
)
def list_orders(
    service: OrderService = Depends(get_order_service),
) -> OrderListResponse:
    orders: Sequence[Order] = service.list_orders()
    return OrderListResponse(orders=[_to_response(order) for order in orders])


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    try:
        return _to_response(service.get_order(order_id))
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def change_order_status(
    order_id: UUID,
    request: ChangeOrderStatusRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    try:
        command = ChangeOrderStatusCommand(
            order_id=order_id,
            status=request.status,
        )
        return _to_response(service.change_status(command))
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except DomainError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(
    order_id: UUID,
    service: OrderService = Depends(get_order_service),
) -> None:
    try:
        service.delete_order(order_id)
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except DomainError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
