from pydantic import BaseModel, EmailStr
from fastapi import Body
from typing import Optional, List
from schemas.vehicles_schema import VehicleDisplay

class UserBase(BaseModel):
    name: str
    surname:str
    e_mail:EmailStr
    password:str
    is_owner:bool = False
    licence_type:str
    licence_date:str


class UserQuery(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    is_owner: Optional[bool] = None
    licence_type: Optional[str] = None
    licence_date: Optional[str] = None


class UserUpdateQuery(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    password: Optional[str] = None
    is_owner: Optional[bool] = None
    licence_type: Optional[str] = None
    licence_date: Optional[str] = None
    

class UserDisplay(BaseModel):
    name:str
    surname:str
    e_mail:EmailStr
    is_owner:Optional[bool]
    licence_type:Optional[str]    
    licence_date:Optional[str]
    owned_vehicles: List[VehicleDisplay] = []
    class Config():
        from_attributes = True


class CurrentUserDisplay(BaseModel):
    user_id:int
    e_mail:EmailStr
    is_owner:Optional[bool]
    licence_type:Optional[str]    
    licence_date:Optional[str]
    is_admin:Optional[bool]
    
   
    






