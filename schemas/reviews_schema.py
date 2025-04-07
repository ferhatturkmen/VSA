from pydantic import BaseModel
from typing import Optional , List, Literal
from enum import Enum

class ReviewBase(BaseModel):
    booking_id: int
    review_type: Literal["renter>owner", "owner>renter", "renter>vehicle"]
    review_rating: int

class ReviewDisplay(BaseModel):
    review_id: int
    booking_id: int
    review_type: Literal["renter>owner", "owner>renter", "renter>vehicle"]
    review_rating: int    
    
class Config():
    from_attributes = True
    
#reviews_schema.py