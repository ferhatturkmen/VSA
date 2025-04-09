from pydantic import BaseModel
from typing import Optional , List
from schemas.files_schema import VehicleFileDisplay
from enum import Enum

class VehicleFuelType(str, Enum):
    benzine = "Benzine"
    diesel = "Diesel"
    electric = "Electric"
    hybrid = "Hybrid"
    lpg = "LPG"
    
    
class VehicleBase(BaseModel):
    plate: str
    brand: str    
    model: str
    year: str
    fuel_type: VehicleFuelType
    total_person: int
    is_commercial: bool
    room_size: float
    is_automatic: bool
    navigation: bool
    air_condition: bool
    include_listing: bool
    owner_id: int

class VehicleQuery(BaseModel):
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    fuel_type: Optional[VehicleFuelType] = None
    total_person: Optional[int] = None  
    is_commercial: Optional[bool] = None  
    room_size: Optional[float] = None
    is_automatic: Optional[bool] = None
    navigation: Optional[bool] = None
    air_condition: Optional[bool] = None
    include_listing: Optional[bool] = None
    owner_id: Optional[int] = None




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
    vehicle_images: List[VehicleFileDisplay] = []
    class Config():
        from_attributes = True


   

