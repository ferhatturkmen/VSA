from pydantic import BaseModel, EmailStr
from fastapi import Body
from typing import Optional, List
from schemas.vehicles_schema import VehicleDisplay

class UserBase(BaseModel):
    user_name: str
    user_surname:str
    e_mail:EmailStr
    password:str
    is_renter:bool = False
    licence_type:str
    licence_date:str


class UserQuery(BaseModel):
    user_name: Optional[str] = None
    user_surname: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    is_renter: Optional[bool] = None
    licence_type: Optional[str] = None
    licence_date: Optional[str] = None
    

class UserDisplay(BaseModel):
    user_name:str
    user_surname:str
    e_mail:EmailStr
    is_renter:Optional[bool]
    licence_type:Optional[str]    
    licence_date:Optional[str]
    owned_vehicles: List[VehicleDisplay] = []
    class Config():
        from_attributes = True


class CurrentUserDisplay(BaseModel):
    user_id:int
    e_mail:EmailStr
    is_renter:Optional[bool]
    licence_type:Optional[str]    
    licence_date:Optional[str]
   
    
   # class Config():
    #    from_attributes = True
 






