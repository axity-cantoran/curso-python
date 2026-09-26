from typing import Protocol


class PricingStrategy(Protocol):
    def calculate(self, price: float) -> float: ...


class RegularPricing:
    def calculate(self, price: float) -> float:
        return price


class DiscountPricing:
    def __init__(self, discount: float) -> None:
        if not 0 <= discount <= 1:
            raise ValueError("El descuento debe estar entre 0 y 1")

        self.discount = discount

    def calculate(self, price: float) -> float:
        return price * (1 - self.discount)


class PremiumPricing:
    def calculate(self, price: float) -> float:
        return price * 0.85


class PriceCalculator:
    def __init__(
        self,
        strategy: PricingStrategy,
    ) -> None:
        self.strategy = strategy

    def calculate(self, price: float) -> float:
        if price < 0:
            raise ValueError("El precio no puede ser negativo")

        return self.strategy.calculate(price)
