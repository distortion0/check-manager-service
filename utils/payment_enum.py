from enum import Enum


class PaymentType(str, Enum):
    cash = "cash"
    cashless = "cashless"