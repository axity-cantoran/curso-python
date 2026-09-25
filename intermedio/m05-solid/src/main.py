import sqlite3

from src.domain import Order
from src.providers import create_repository
from src.services import OrderService


def ejecutar(kind: str) -> Order | None:
    connection = sqlite3.connect(":memory:")

    try:
        repository = create_repository(
            kind,
            connection if kind == "sql" else None,
        )
        service = OrderService(repository)

        order = Order(
            order_id=1,
            product="Teclado",
            quantity=2,
            unit_price=50.0,
        )

        service.create_order(order)
        return service.get_order(1)
    finally:
        connection.close()


def main() -> None:
    memory_order = ejecutar("memory")
    sql_order = ejecutar("sql")

    print(memory_order)
    print(sql_order)
    print(memory_order == sql_order)


if __name__ == "__main__":
    main()
