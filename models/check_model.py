import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON, Float, String, Enum
from sqlalchemy.orm import relationship

from db_utils.base import Base
from utils.payment_enum import PaymentType


class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Float)
    rest = Column(Float)
    payment_type = Column(Enum(PaymentType), nullable=False)
    payment_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    additional_data = Column(JSON, nullable=True)
    public_token = Column(String, unique=True, default=lambda: uuid.uuid4().hex)

    user = relationship("User")
    products = relationship("CheckProduct", back_populates="check")

    def calculate_total(self):
        self.total = round(sum(p.total for p in self.products), 2)

    def calculate_rest(self):
        rest = round(self.payment_amount - self.total, 2)
        if rest < 0:
            raise ValueError("Payment amount is less than total amount due")  # <-- I suppose it cannot be minus
        self.rest = rest

    def to_dict(self):
        return {
            "id": self.id,
            "products": [
                {
                    "name": p.name,
                    "price": p.price,
                    "quantity": p.quantity,
                    "total": p.total,
                }
                for p in self.products
            ],
            "payment": {
                "type": self.payment_type,
                "amount": self.payment_amount,
            },
            "total": self.total,
            "rest": self.rest,
            "created_at": self.created_at,
        }


class CheckProduct(Base):
    __tablename__ = "check_products"

    id = Column(Integer, primary_key=True)
    check_id = Column(Integer, ForeignKey("checks.id"))
    name = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    total = Column(Float)

    check = relationship("Check", back_populates="products")

    def calculate_total(self):
        self.total = round(self.price * self.quantity, 2)
