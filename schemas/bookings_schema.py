from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    vehicle_id: int
    start_time: datetime
    end_time: datetime