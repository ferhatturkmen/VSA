from pydantic import BaseModel
from typing import Optional , List
from datetime import datetime
from enum import Enum


class PaymentStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"

class PaymentBase(BaseModel):
    payment_amount: Optional[float] = None
    status: Optional[PaymentStatus] = "pending"
    payment_approved_at: Optional[datetime] = None
    booking_id: Optional[int] = None

class PaymentDisplay(BaseModel):
    payment_id:int
    payment_amount:float
    status:str
    booking_id:int
    class Config():
        from_attributes = True


    



    
