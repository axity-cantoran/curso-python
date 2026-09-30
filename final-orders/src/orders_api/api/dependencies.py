from collections.abc import Generator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from orders_api.application.services import OrderService
from orders_api.infrastructure.config import get_settings
from orders_api.infrastructure.database import get_session
from orders_api.infrastructure.repositories import SqlAlchemyOrderRepository


def require_api_key(
    x_api_key: str | None = Header(default=None),
) -> None:
    settings = get_settings()

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida.",
        )


def get_order_service(
    session: Session = Depends(get_session),
) -> Generator[OrderService, None, None]:
    repository = SqlAlchemyOrderRepository(session)
    yield OrderService(repository)
