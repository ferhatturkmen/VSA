from pydantic import BaseModel
from fastapi import Body
from typing import Optional


class VehiclePropertyCreate(BaseModel):
    daily_rate: float
    location: str
    unavailable_dates: Optional[str] = None
    vehicle_id: int


class VehiclePropertyEditing(BaseModel):
    daily_rate: Optional[float] = None
    location: Optional[str] = None
    unavailable_dates: Optional[str] = None
    vehicle_id: Optional[int] = None 
    class Config:
        from_attributes = True



class VehiclePropertyOut(VehiclePropertyCreate):
    property_id: int

    class Config:
        from_attributes = True