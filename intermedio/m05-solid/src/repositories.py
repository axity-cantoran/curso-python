import sqlite3

from src.domain import Order


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)


class SqlOrderRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL
            )
            """
        )
        self._connection.commit()

    def save(self, order: Order) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO orders (
                order_id,
                product,
                quantity,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                order.order_id,
                order.product,
                order.quantity,
                order.unit_price,
            ),
        )
        self._connection.commit()

    def get(self, order_id: int) -> Order | None:
        fila = self._connection.execute(
            """
            SELECT order_id, product, quantity, unit_price
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,),
        ).fetchone()

        if fila is None:
            return None

        return Order(
            order_id=fila[0],
            product=fila[1],
            quantity=fila[2],
            unit_price=fila[3],
        )
