class DomainError(Exception):
    """Error base del dominio."""


class InvalidQuantityError(DomainError):
    """La cantidad del producto no es válida."""


class ProductNotFoundError(DomainError):
    """El producto no existe en el catálogo."""


class InvalidOrderStatusError(DomainError):
    """La transición de estado no está permitida."""
