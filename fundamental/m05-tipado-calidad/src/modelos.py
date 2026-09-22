from pydantic import BaseModel, Field, field_validator


class OrderIn(BaseModel):
    order_id: str = Field(min_length=1)
    product: str = Field(min_length=1)
    unit_price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    tax_rate: float = Field(ge=0, le=1)

    @field_validator("order_id", "product")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
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
