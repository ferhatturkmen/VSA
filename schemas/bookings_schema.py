from pydantic import BaseModel
from datetime import datetime
from typing import Optional , List

from schemas.users_schema import UserDisplay
from schemas.vehicles_schema import VehicleDisplay

class BookingBase(BaseModel):
    rented_vehicle_id: int
    start_time: datetime
    end_time: datetime

class BookingDisplay(BaseModel):
    booking_id: int
    booking_date: datetime
    start_time: datetime
    end_time: datetime
    total_days: int

    is_cancelled: Optional[bool] = None
    cancelled_at: Optional[datetime] = None
    cancellation_type: Optional[str] = None

    is_delivered_up: Optional[bool] = None
    damage_report: Optional[str] = None
    is_report_approved: Optional[bool] = None
    class Config:
        from_attributes = True
    
    
