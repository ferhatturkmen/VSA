from pydantic import BaseModel
from fastapi import Body
from typing import Optional


class VehiclePropertyCreate(BaseModel):
    daily_rate: float
    location: str
    unavailable_dates: Optional[str] = None
    vehicle_id: int


# class VehiclePropertyDisplay(BaseModel):
#     daily_rate: float
#     location: str
#     unavailable_dates: Optional[str] = None
#     vehicle_id: int



class VehiclePropertyOut(VehiclePropertyCreate):
    property_id: int