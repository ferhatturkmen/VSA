from pydantic import BaseModel
from typing import Optional, List
from schemas.vehicles_schema import VehicleDisplay

class UserBase(BaseModel):
    user_name: str
    user_surname:str
    e_mail:str
    password:str
    is_renter:bool
    licence_type:str
    licence_date:str
    

class UserDisplay(BaseModel):
    user_name:str
    user_surname:str
    e_mail:str
    is_renter:Optional[bool]
    licence_type:Optional[str]    
    licence_date:Optional[str]
    owned_vehicles: List[VehicleDisplay] = []
    class Config():
        from_attributes = True

   # class Config():
    #    from_attributes = True
 






