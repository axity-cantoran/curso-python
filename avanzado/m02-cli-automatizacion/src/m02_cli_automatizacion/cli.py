import httpx
import typer

from .client import OrdersApiClient
from .config import load_settings

app = typer.Typer(
    name="orders",
    help="Gestiona órdenes mediante una API.",
)


def create_client() -> OrdersApiClient:
    return OrdersApiClient(load_settings())


@app.command("list")
def list_orders() -> None:
    client = create_client()

    try:
        orders = client.list_orders()

        for order in orders:
            typer.echo(
                f"{order['id']}: {order['product']} - {order['quantity']} unidades"
            )
    except (httpx.HTTPError, ValueError) as error:
        typer.echo(
            f"Error al listar órdenes: {error}",
            err=True,
        )
        raise typer.Exit(code=1)
    finally:
        client.close()


@app.command("create")
def create_order(
    product: str = typer.Option(
        ...,
        "--product",
        help="Nombre del producto",
    ),
    quantity: int = typer.Option(
        ...,
        "--quantity",
        min=1,
        help="Cantidad de productos",
    ),
    unit_price: float = typer.Option(
        ...,
        "--unit-price",
        min=0,
        help="Precio unitario",
    ),
) -> None:
    client = create_client()

    try:
        order = client.create_order(
            product=product,
            quantity=quantity,
            unit_price=unit_price,
        )

        typer.echo(f"Orden creada: {order['id']}")
    except (httpx.HTTPError, ValueError) as error:
        typer.echo(
            f"Error al crear la orden: {error}",
            err=True,
        )
        raise typer.Exit(code=1)
    finally:
        client.close()


@app.command("delete")
def delete_order(
    order_id: int = typer.Argument(
        ...,
        min=1,
        help="Identificador de la orden",
    ),
) -> None:
    client = create_client()

    try:
        client.delete_order(order_id)
        typer.echo(f"Orden eliminada: {order_id}")
    except (httpx.HTTPError, ValueError) as error:
        typer.echo(
            f"Error al eliminar la orden: {error}",
            err=True,
        )
        raise typer.Exit(code=1)
    finally:
        client.close()


if __name__ == "__main__":
    app()
