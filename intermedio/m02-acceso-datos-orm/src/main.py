from src.base_datos import SessionLocal, engine
from src.modelos import Base
from src.repositorio import (
    agregar_item,
    crear_orden,
    crear_usuario,
    listar_ordenes_de_usuario,
)


def main() -> None:
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        usuario = crear_usuario(
            session,
            name="Ana",
            email="ana@example.com",
        )

        orden = crear_orden(session, usuario)

        agregar_item(
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

        print(f"Usuario: {usuario.name}")
        print(f"Órdenes: {len(ordenes)}")


if __name__ == "__main__":
    main()
