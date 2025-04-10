from pydantic import BaseModel, EmailStr
from fastapi import Body
from typing import Optional, List
from schemas.vehicles_schema import VehicleDisplay
from datetime import date, datetime
from enum import Enum

class LicenceType(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"

class UserCreate(BaseModel):
    name: str = Body(..., min_length=2, max_length=25)
    surname: str = Body(..., min_length=2, max_length=25)
    e_mail: EmailStr = Body(..., min_length=5, max_length=50)
    password: str = Body(..., min_length=8, max_length=25)    
    licence_type: LicenceType
    licence_date: date

class UserBase(BaseModel):
    name: str
    surname:str
    e_mail:EmailStr
    password:str
    is_owner:bool = False
    licence_type:LicenceType
    licence_date:date


class UserQuery(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    is_owner: Optional[bool] = None
    licence_type: Optional[LicenceType] = None
    licence_date: Optional[date] = None


class UserUpdateQuery(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    e_mail: Optional[EmailStr] = None
    password: Optional[str] = None
   # is_owner: Optional[bool] = None
    licence_type: Optional[LicenceType] = None
    licence_date: Optional[date] = None
    is_admin: Optional[bool]
    

class UserDisplay(BaseModel):
    name:str
    surname:str
    e_mail:EmailStr
    is_owner:Optional[bool]
    licence_type:Optional[LicenceType]    
    licence_date:Optional[date]
    owned_vehicles: List[VehicleDisplay] = []
    class Config():
        from_attributes = True


class CurrentUserDisplay(BaseModel):
    user_id:int
    e_mail:EmailStr
    is_owner:Optional[bool]
    licence_type:Optional[LicenceType]    
    licence_date:Optional[date]
    is_admin:Optional[bool]

   
    






