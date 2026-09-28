from typing import Any

import httpx

from .config import Settings


class OrdersApiClient:
    def __init__(self, settings: Settings) -> None:
        headers: dict[str, str] = {}

        if settings.api_token:
            headers["Authorization"] = f"Bearer {settings.api_token}"

        self.client = httpx.Client(
            base_url=settings.api_url,
            timeout=settings.timeout,
            headers=headers,
        )

    def list_orders(self) -> list[dict[str, Any]]:
        response = self.client.get("/orders/")
        response.raise_for_status()
        return response.json()

    def create_order(
        self,
        product: str,
        quantity: int,
        unit_price: float,
    ) -> dict[str, Any]:
        response = self.client.post(
            "/orders/",
            json={
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
            },
        )
        response.raise_for_status()
        return response.json()

    def delete_order(self, order_id: int) -> None:
        response = self.client.delete(f"/orders/{order_id}")
        response.raise_for_status()

    def close(self) -> None:
        self.client.close()
