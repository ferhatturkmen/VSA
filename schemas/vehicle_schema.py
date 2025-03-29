from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    plate: str
    brand: str    
    model: str
    year: str
    fuel_type: str
    total_person: int
    is_commercial: bool
    room_size: float
    is_automatic: bool
    include_listing: bool
    owner_id: int


class VehicleDisplay(BaseModel):
    plate: str
    brand: str
    model: str
    year: str
    fuel_type: str
    total_person: int  
    is_commercial: bool  
    room_size: float
    is_automatic: bool
    class Config():
        from_attributes = True

   

