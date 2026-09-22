from pydantic import BaseModel, Field, field_validator


class OrderIn(BaseModel):
    order_id: str = Field(min_length=1)  # Al menos un carácter
    product: str = Field(min_length=1)
    unit_price: float = Field(gt=0)  # Precio mayor que cero
    quantity: int = Field(gt=0)
    tax_rate: float = Field(
        ge=0, le=1
    )  # Permite valores entre 0 y 1, incluyendo ambos extremos

    @field_validator("order_id", "product")
    @classmethod
    def text_must_not_be_blank(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("El texto no puede estar vacío")

        return value


class OrderOut(BaseModel):
    order_id: str
    product: str
    unit_price: float
    quantity: int
    tax_rate: float
    subtotal: float
    tax: float
    total: float


# Bloque de prueba
"""
if __name__ == "__main__":
    order_in = OrderIn(
    order_id="ORD-002",
    product="Monitor",
    unit_price="200",
    quantity="2",
    tax_rate="0.16",
    )  

    print(order_in)
    print(order_in.model_dump())
    print(order_in.model_dump_json())
"""
