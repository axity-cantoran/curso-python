from dataclasses import dataclass

from orders_api.domain.enums import ProductCategory


@dataclass(frozen=True, slots=True)
class Product:
    id: str
    name: str
    category: ProductCategory


CATALOG: dict[str, Product] = {
    "caballero": Product(
        id="caballero",
        name="Caballero",
        category=ProductCategory.FIGURES,
    ),
    "mago": Product(
        id="mago",
        name="Mago",
        category=ProductCategory.FIGURES,
    ),
    "robot": Product(
        id="robot",
        name="Robot",
        category=ProductCategory.FIGURES,
    ),
    "alienigena": Product(
        id="alienigena",
        name="Alienígena",
        category=ProductCategory.FIGURES,
    ),
    "accesorios": Product(
        id="accesorios",
        name="Accesorios",
        category=ProductCategory.COMPLEMENTS,
    ),
    "herramientas": Product(
        id="herramientas",
        name="Herramientas",
        category=ProductCategory.COMPLEMENTS,
    ),
}


def get_product(product_id: str) -> Product:
    try:
        return CATALOG[product_id]
    except KeyError as error:
        raise ValueError(f"Producto no encontrado: {product_id}") from error
