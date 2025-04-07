from sqlalchemy.orm.session import Session
from schemas.reviews_schema import ReviewBase, ReviewQuery
from db.models import db_review
from fastapi import HTTPException, status, Query
from typing import List, Optional

def create_review(db:Session, request: ReviewBase):
    new_review = db_review(
        booking_id=request.booking_id,
        review_type=request.review_type,
        review_rating=request.review_rating
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_review(db:Session, review_id:int):
      req_review = db.query(db_review).filter(db_review.review_id == review_id).first()
      if not req_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested review with id {review_id} is not found')
      return req_review
  
def get_all_review(db: Session, query_params: Optional[ReviewQuery]):
  req_db_query = db.query(db_review)
  if query_params:
    if query_params.review_id:
      req_db_query = req_db_query.filter(db_review.review_id == query_params.review_id)
    if query_params.booking_id:
        req_db_query = req_db_query.filter(db_review.booking_id == query_params.booking_id)
    if query_params.review_type:
        req_db_query = req_db_query.filter(db_review.review_type == query_params.review_type)
    if query_params.review_rating:
        req_db_query = req_db_query.filter(db_review.review_rating == query_params.review_rating)
  return req_db_query.all()
   
#reviews_contrpoller.py