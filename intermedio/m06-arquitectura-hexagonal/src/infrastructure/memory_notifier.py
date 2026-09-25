from src.domain.entities import Order


class InMemoryOrderNotifier:
    def __init__(self) -> None:
        self.notifications: list[Order] = []

    def notify_order_created(self, order: Order) -> None:
        self.notifications.append(order)
