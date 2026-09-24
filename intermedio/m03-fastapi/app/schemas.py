from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    product: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderUpdate(BaseModel):
    product: str | None = Field(default=None, min_length=1)
    quantity: int | None = Field(default=None, gt=0)
    unit_price: float | None = Field(default=None, gt=0)


class OrderOut(BaseModel):
    id: int
    product: str
    quantity: int
    unit_price: float

    model_config = {
        "from_attributes": True,
    }


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    model_config = {
        "from_attributes": True,
    }
