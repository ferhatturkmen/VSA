from pydantic import BaseModel
from typing import Optional , List
from schemas.files_schema import 


class PaymentBase(BaseModel):
    payment_amount:float
    status:str
    payment_approved_at:Optional[datetime]
    booking_id:int



    
