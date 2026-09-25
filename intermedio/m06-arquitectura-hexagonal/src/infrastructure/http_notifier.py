import httpx

from src.domain.entities import Order


class HttpOrderNotifier:
    def __init__(
        self,
        client: httpx.Client,
        url: str,
    ) -> None:
        self.client = client
        self.url = url

    def notify_order_created(self, order: Order) -> None:
        response = self.client.post(
            self.url,
            json={
                "order_id": order.order_id,
                "product": order.product,
                "total": order.total,
            },
        )
        response.raise_for_status()
