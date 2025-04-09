from fastapi import APIRouter, Depends
from schemas.reviews_schema import ReviewBase, ReviewDisplay, ReviewQuery
from schemas.users_schema import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import reviews_controller
from typing import List, Optional
from auth.oauth2 import oauth2_schema
from auth.oauth2 import get_current_user
router = APIRouter(
    prefix = "/reviews",
    tags = ["reviews"]
)

#create a new review
@router.post("/new", response_model=ReviewDisplay)
def create_review(request:ReviewBase, current_user:UserBase=Depends(get_current_user), db : Session = Depends(get_db)):
    return reviews_controller.create_review(db, request)


#read all reviews
@router.get("/all",) # response_model=List[ReviewDisplay])
def get_all_reviews(db: Session = Depends(get_db),                    
                    query_params: ReviewQuery = Depends()):
    req_db_query = reviews_controller.get_all_review(db, query_params=query_params)
    return {
        "data":req_db_query
    }


#read review by id 
@router.get("/{review_id}", response_model=ReviewDisplay)
def get_review(review_id:int, current_user:UserBase=Depends(get_current_user), db:Session=Depends(get_db)):
    return reviews_controller.get_review(db, review_id)


#update a review by id 
@router.put("/{review_id}/update", response_model=ReviewDisplay)
def update_review(review_id:int, request:ReviewQuery, current_user:UserBase=Depends(get_current_user), db:Session=Depends(get_db)):
    return reviews_controller.update_review(db, review_id, request)

#delete a review by id 
@router.delete("/{review_id}/delete")
def delete_review(review_id:int, current_user:UserBase=Depends(get_current_user), db:Session=Depends(get_db)):
    return reviews_controller.delete_review(db, review_id)

#reviews_router.py