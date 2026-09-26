from unittest.mock import Mock

import pytest

from src.adapters import ExternalPriceAdapter
from src.cache import cached
from src.pricing import (
    DiscountPricing,
    PremiumPricing,
    PriceCalculator,
    RegularPricing,
)


@pytest.mark.parametrize(
    ("strategy", "expected"),
    [
        (RegularPricing(), 100.0),
        (DiscountPricing(0.10), 90.0),
        (PremiumPricing(), 85.0),
    ],
)
def test_pricing_strategies(
    strategy,
    expected: float,
) -> None:
    calculator = PriceCalculator(strategy)

    assert calculator.calculate(100.0) == expected


def test_negative_price_is_rejected() -> None:
    calculator = PriceCalculator(RegularPricing())

    with pytest.raises(ValueError, match="negativo"):
        calculator.calculate(-1.0)


def test_cache_avoids_repeated_execution() -> None:
    function = Mock(return_value=20.0)
    cached_function = cached(function)

    assert cached_function(10.0) == 20.0
    assert cached_function(10.0) == 20.0

    function.assert_called_once_with(10.0)


def test_external_adapter_translates_response() -> None:
    service = Mock()
    service.fetch_current_price.return_value = {
        "code": "SKU-001",
        "amount": 100.0,
    }

    adapter = ExternalPriceAdapter(service)

    assert adapter.get_price("SKU-001") == 100.0
    service.fetch_current_price.assert_called_once_with("SKU-001")


def test_external_adapter_rejects_invalid_amount() -> None:
    service = Mock()
    service.fetch_current_price.return_value = {
        "code": "SKU-001",
        "amount": "invalid",
    }

    adapter = ExternalPriceAdapter(service)

    with pytest.raises(TypeError, match="numérico"):
        adapter.get_price("SKU-001")
