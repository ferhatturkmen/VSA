from pydantic import BaseModel, Field
from datetime import datetime,date,timedelta
from typing import Optional , List

from schemas.users_schema import UserDisplay
from schemas.vehicles_schema import VehicleDisplay

class BookingBase(BaseModel):
    rented_vehicle_id: int
    booking_date: date 
    total_days: int = 1 

class BookingDisplay(BaseModel):
    booking_id: int
    booking_date: date # When the rental starts
    total_days: int
    created_at: datetime # When the booking was made
    approved_at: Optional[datetime] = None
        
    is_delivered_up: Optional[bool] = None
    damage_report: Optional[str] = None
    is_report_approved: Optional[bool] = None

    is_cancelled: Optional[bool] = None
    cancelled_at: Optional[datetime] = None
    cancellation_type: Optional[str] = None

    
    class Config:
        from_attributes = True
    
    
