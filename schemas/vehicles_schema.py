from pydantic import BaseModel
from typing import Optional , List

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
    navigation: bool
    air_condition: bool
    include_listing: bool
    owner_id: int

class VehicleImageDisplay(BaseModel):
    image_id: int
    filename: Optional[str]
    image_url: Optional[str]
    vehicle_id: Optional[int] #don't forget to delete Optional
    class Config():
        from_attributes = True


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
    navigation: bool
    air_condition: bool
    include_listing: bool
    owner_id: int
    vehicle_images: List[VehicleImageDisplay] = []
    class Config():
        from_attributes = True


   

