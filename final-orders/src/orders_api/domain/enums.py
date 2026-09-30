from enum import StrEnum


class ProductCategory(StrEnum):
    FIGURES = "FIGURES"
    COMPLEMENTS = "COMPLEMENTS"


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
