from fastapi import APIRouter, Depends
from schemas.reviews_schema import ReviewBase, ReviewDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import reviews_controller
from typing import List, Optional

router = APIRouter(
    prefix = "/reviews",
    tags = ["reviews"]
)

#create a new review
@router.post("/", response_model=ReviewDisplay)
def create_review(request:ReviewBase, db : Session = Depends(get_db)):
    return reviews_controller.create_review(db, request)

#read review by id 
@router.get("/{vehicle_id}", response_model=ReviewDisplay)
def get_review(vehicle_id:int, db:Session=Depends(get_db)):
    return reviews_controller.get_review(db, vehicle_id)

#read all reviews
@router.get("/", response_model=List[ReviewDisplay])
def get_all_reviews(db: Session = Depends(get_db)):
    return reviews_controller.get_all_review(db)

#reviews_router.py