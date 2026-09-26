from src.adapters import (
    ExternalPriceAdapter,
    ExternalPriceService,
)
from src.cache import cached
from src.pricing import (
    DiscountPricing,
    PriceCalculator,
)


@cached
def obtener_precio(
    provider: ExternalPriceAdapter,
    product_id: str,
) -> float:
    return provider.get_price(product_id)


def main() -> None:
    provider = ExternalPriceAdapter(ExternalPriceService())

    precio = obtener_precio(provider, "SKU-001")

    calculator = PriceCalculator(DiscountPricing(0.10))

    precio_final = calculator.calculate(precio)

    print(f"Precio base: {precio}")
    print(f"Precio final: {precio_final}")


if __name__ == "__main__":
    main()
