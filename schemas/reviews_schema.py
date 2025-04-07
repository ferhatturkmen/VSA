from pydantic import BaseModel, Field
from typing import Optional , List
from enum import Enum

class ReviewType(str, Enum):
    renter_to_owner = "renter>owner"
    owner_to_renter = "owner>renter"
    renter_to_vehicle = "renter>vehicle"

class ReviewBase(BaseModel):
    booking_id: int
    review_type: ReviewType
    review_rating: int 


class ReviewQuery(BaseModel):
    review_id: Optional[int] = None
    booking_id: Optional[int] = None
    review_type: Optional[ReviewType] = None
    review_rating: Optional[int] = None


class ReviewDisplay(BaseModel):
    review_id: int
    booking_id: int
    review_type: ReviewType
    review_rating: int  
    class Config():
        from_attributes = True
    
#reviews_schema.py