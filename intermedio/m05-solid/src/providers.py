import sqlite3
from collections.abc import Callable

from src.ports import OrderRepository
from src.repositories import (
    InMemoryOrderRepository,
    SqlOrderRepository,
)

RepositoryProvider = Callable[[], OrderRepository]


def provide_memory_repository() -> OrderRepository:
    return InMemoryOrderRepository()


def provide_sql_repository(
    connection: sqlite3.Connection,
) -> OrderRepository:
    return SqlOrderRepository(connection)


def create_repository(
    kind: str,
    connection: sqlite3.Connection | None = None,
) -> OrderRepository:
    if kind == "memory":
        return provide_memory_repository()

    if kind == "sql":
        if connection is None:
            raise ValueError("La conexión es obligatoria para SQL")

        return provide_sql_repository(connection)

    raise ValueError(f"Tipo de repositorio desconocido: {kind}")
