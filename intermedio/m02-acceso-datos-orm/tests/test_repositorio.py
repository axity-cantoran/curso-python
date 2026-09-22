import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.modelos import User
from src.repositorio import (
    actualizar_nombre_usuario,
    agregar_item,
    crear_orden,
    crear_usuario,
    eliminar_item,
    listar_ordenes_de_usuario,
    obtener_usuario,
)


def test_crear_usuario(session: Session) -> None:
    usuario = crear_usuario(
        session,
        name="Ana",
        email="ana@example.com",
    )

    resultado = obtener_usuario(session, usuario.id)

    assert resultado is not None
    assert resultado.name == "Ana"
    assert resultado.email == "ana@example.com"


def test_crear_orden_con_item(session: Session) -> None:
    usuario = crear_usuario(
        session,
        name="Luis",
        email="luis@example.com",
    )

    orden = crear_orden(session, usuario)

    item = agregar_item(
        session,
        order=orden,
        product="Teclado",
        quantity=2,
        unit_price=50.0,
    )

    ordenes = listar_ordenes_de_usuario(
        session,
        usuario.id,
    )

    assert len(ordenes) == 1
    assert ordenes[0].id == orden.id
    assert item.order_id == orden.id


def test_actualizar_usuario(session: Session) -> None:
    usuario = crear_usuario(
        session,
        name="Ana",
        email="ana@example.com",
    )

    actualizado = actualizar_nombre_usuario(
        session,
        usuario,
        "Ana García",
    )

    assert actualizado.name == "Ana García"


def test_eliminar_item(session: Session) -> None:
    usuario = crear_usuario(
        session,
        name="Luis",
        email="luis@example.com",
    )

    orden = crear_orden(session, usuario)

    item = agregar_item(
        session,
        order=orden,
        product="Mouse",
        quantity=1,
        unit_price=25.0,
    )

    eliminar_item(session, item)

    assert item.id is not None


def test_email_duplicado_produce_rollback(session: Session) -> None:
    crear_usuario(
        session,
        name="Ana",
        email="ana@example.com",
    )

    usuario_duplicado = User(
        name="Otra Ana",
        email="ana@example.com",
    )

    session.add(usuario_duplicado)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()

    usuarios = session.query(User).all()

    assert len(usuarios) == 1
