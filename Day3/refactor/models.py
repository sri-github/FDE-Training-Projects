# from pydantic import BaseModel
# class Invoice(BaseModel):
#     invoice_id: int
#     amount: float
#     status: str
#     vendor: str="UNKNOWN"

from typing import Optional
from pydantic import BaseModel

class Payment(BaseModel):
    invoice_id: str
    paid: float

class PaymentUpdate(BaseModel):
    paid: Optional[float] = None