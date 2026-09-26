from typing import Protocol


class PriceProvider(Protocol):
    def get_price(self, product_id: str) -> float: ...


class ExternalPriceService:
    def fetch_current_price(
        self,
        external_code: str,
    ) -> dict[str, object]:
        return {
            "code": external_code,
            "amount": 100.0,
        }


class ExternalPriceAdapter:
    def __init__(
        self,
        service: ExternalPriceService,
    ) -> None:
        self.service = service

    def get_price(self, product_id: str) -> float:
        response = self.service.fetch_current_price(product_id)

        amount = response["amount"]

        if not isinstance(amount, (int, float)):
            raise TypeError("El precio no es numérico")

        return float(amount)
