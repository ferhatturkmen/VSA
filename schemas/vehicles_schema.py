from pydantic import BaseModel
from typing import Optional , List
from schemas.files_schema import VehicleImageDisplay
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
    is_automatic: bool
    navigation: bool
    air_condition: bool
    include_listing: bool
    daily_rate: float
    location: str
    owner_id: int

class VehicleQuery(BaseModel):
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    fuel_type: Optional[VehicleFuelType] = None
    total_person: Optional[int] = None  
    is_commercial: Optional[bool] = None  
    is_automatic: Optional[bool] = None
    navigation: Optional[bool] = None
    air_condition: Optional[bool] = None
    include_listing: Optional[bool] = None
    daily_rate: Optional[float] = None
    location: Optional[str] = None
    owner_id: Optional[int] = None




class VehicleDisplay(BaseModel):
    plate: str
    brand: str
    model: str
    year: str
    fuel_type: VehicleFuelType
    total_person: int  
    is_commercial: bool  
    is_automatic: bool
    navigation: bool
    air_condition: bool
    include_listing: bool
    daily_rate: float
    location: str
    owner_id: int
    vehicle_images: List[VehicleImageDisplay] = []
    class Config():
        from_attributes = True


   

