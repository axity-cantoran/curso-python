from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modelos import Order, OrderItem, User


def crear_usuario(
    session: Session,
    name: str,
    email: str,
) -> User:
    usuario = User(name=name, email=email)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def crear_orden(
    session: Session,
    user: User,
) -> Order:
    orden = Order(user=user)
    session.add(orden)
    session.commit()
    session.refresh(orden)
    return orden


def agregar_item(
    session: Session,
    order: Order,
    product: str,
    quantity: int,
    unit_price: float,
) -> OrderItem:
    item = OrderItem(
        order=order,
        product=product,
        quantity=quantity,
        unit_price=unit_price,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def obtener_usuario(
    session: Session,
    user_id: int,
) -> User | None:
    return session.get(User, user_id)


def obtener_orden(
    session: Session,
    order_id: int,
) -> Order | None:
    return session.get(Order, order_id)


def listar_ordenes_de_usuario(
    session: Session,
    user_id: int,
) -> list[Order]:
    consulta = select(Order).where(Order.user_id == user_id)
    return list(session.scalars(consulta).all())


def actualizar_nombre_usuario(
    session: Session,
    user: User,
    nuevo_nombre: str,
) -> User:
    user.name = nuevo_nombre
    session.commit()
    session.refresh(user)
    return user


def eliminar_item(
    session: Session,
    item: OrderItem,
) -> None:
    session.delete(item)
    session.commit()
