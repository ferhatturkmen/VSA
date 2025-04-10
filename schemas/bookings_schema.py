from pydantic import BaseModel, Field
from datetime import datetime,date,timedelta
from typing import Optional , List
from schemas.users_schema import UserDisplay
from schemas.vehicles_schema import VehicleDisplay

class BookingBase(BaseModel):
    rented_vehicle_id: int 
   # renter_id: int 
    start_date: date
    end_date: date
   # created_at: datetime = Field(default_factory=datetime.now, title="Created At", description="Booking creation date and time")
   # is_delivered_up: bool = False
   # damage_report: Optional[str] = None
   # is_report_approved: bool = False
   # approved_at: Optional[datetime] = None
   # is_cancelled: bool = False
   # cancelled_at: Optional[datetime] = None

        
    

class BookingDisplay(BaseModel):
    booking_id:int
    rented_vehicle_id:int
    renter_id:int
    start_date:date
    end_date:date
    created_at:datetime
    is_delivered_up:bool
    damage_report:Optional[str]
    is_report_approved:bool
    approved_at:Optional[datetime]
    is_cancelled:bool
    cancelled_at:Optional[datetime]
    class Config:
        from_attributes = True

class BookingQuery(BaseModel):
    booking_id: Optional[int] = None
    rented_vehicle_id: Optional[int] = None
    renter_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: Optional[datetime] = None
    is_delivered_up: Optional[bool] = False
    damage_report: Optional[str] = None
    is_report_approved: Optional[bool] = False
    approved_at: Optional[datetime] = None
    is_cancelled: Optional[bool] = False
    cancelled_at: Optional[datetime] = None
    
    
