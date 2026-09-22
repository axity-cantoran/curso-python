from pydantic import ValidationError

from entidades import Order
from modelos import OrderIn, OrderOut


def order_in_to_entity(order_in: OrderIn) -> Order:
    return Order(
        order_id=order_in.order_id,
        product=order_in.product,
        unit_price=order_in.unit_price,
        quantity=order_in.quantity,
        tax_rate=order_in.tax_rate,
    )


def order_to_order_out(order: Order) -> OrderOut:
    return OrderOut(
        order_id=order.order_id,
        product=order.product,
        unit_price=order.unit_price,
        quantity=order.quantity,
        tax_rate=order.tax_rate,
        subtotal=order.subtotal,
        tax=order.tax,
        total=order.total,
    )


def main() -> None:
    try:
        order_in = OrderIn(
            order_id="ORD-001",
            product="Teclado",
            unit_price=50,
            quantity=2,
            tax_rate=0.16,
        )
    except ValidationError as error:
        print(f"Datos inválidos:\n{error}")
        return

    order = order_in_to_entity(order_in)
    order_out = order_to_order_out(order)

    another_order = Order(
        order_id="ORD-002",
        product="Monitor",
        unit_price=200,
        quantity=1,
        tax_rate=0.16,
    )

    print(order)
    # print(order == order_out)
    print(order_out.model_dump())
    print(order_out.model_dump_json())

    print(order == another_order)
    print(order < another_order)


if __name__ == "__main__":
    main()
