from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import Order, User
from app.schemas import OrderCreate, OrderOut, OrderUpdate

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order_data: OrderCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Order:
    order = Order(
        product=order_data.product,
        quantity=order_data.quantity,
        unit_price=order_data.unit_price,
        user_id=current_user.id,
    )

    session.add(order)
    session.commit()
    session.refresh(order)

    return order


@router.get(
    "/",
    response_model=list[OrderOut],
)
def list_orders(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Order]:
    query = select(Order).where(Order.user_id == current_user.id)
    return list(session.scalars(query).all())


@router.get(
    "/{order_id}",
    response_model=OrderOut,
)
def get_order(
    order_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Order:
    order = session.get(Order, order_id)

    if order is None or order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return order


@router.put(
    "/{order_id}",
    response_model=OrderOut,
)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Order:
    order = session.get(Order, order_id)

    if order is None or order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    cambios = order_data.model_dump(exclude_unset=True)

    for campo, valor in cambios.items():
        setattr(order, campo, valor)

    session.commit()
    session.refresh(order)

    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(
    order_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    order = session.get(Order, order_id)

    if order is None or order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    session.delete(order)
    session.commit()
