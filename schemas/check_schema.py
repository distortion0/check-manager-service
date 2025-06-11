from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from utils.payment_enum import PaymentType


class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="Price must be greater than 0")
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")


class Payment(BaseModel):
    type: PaymentType
    amount: float = Field(gt=0, description="Amount must be greater than 0")


class CheckCreate(BaseModel):
    products: List[Product]
    payment: Payment
    additional_data: Optional[dict] = None


class ProductResponse(BaseModel):
    name: str
    price: float
    quantity: int
    total: float

    class Config:
        from_attributes = True


class PaymentResponse(BaseModel):
    type: str
    amount: float


class CheckResponse(BaseModel):
    id: int
    products: List[ProductResponse]
    payment: PaymentResponse
    total: float
    rest: float
    additional_data: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CheckFilter(BaseModel):
    date_from: Optional[datetime] = Field(None, description="Date create from")
    date_to: Optional[datetime] = Field(None, description="Date create to")
    min_total: Optional[float] = Field(None, description="Total price minimum")
    payment_type: Optional[str] = Field(None, description="type of payment")
    limit: int = Field(10, ge=10, le=100, description="items quantity per page")
    offset: int = Field(0, ge=0, description="offset")

    class Config:
        extra = "forbid"
