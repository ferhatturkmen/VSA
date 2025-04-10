from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from db.database import get_db
from db.models import DbUser
from auth.oauth2 import get_current_user
from schemas.users_schema import UserBase
from schemas.bookings_schema import BookingBase, BookingDisplay, BookingQuery
from controllers import bookings_controller
from utils.user_utils import check_booker, check_admin

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)


# Create a new booking
@router.post("/", response_model=BookingDisplay)
def create_booking(request: BookingBase,
                   current_user: UserBase = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return bookings_controller.create_booking(db, request, current_user)


# Read all bookings
@router.get("/", response_model=List[BookingQuery])
def get_all_bookings(db: Session = Depends(get_db),
                     current_user: UserBase = Depends(get_current_user),
                     query_params: BookingQuery = Depends(),
                     ):
    check_admin(current_user)
    req_db_query = bookings_controller.get_all_bookings(db, query_params=query_params)
    return req_db_query
        
# Read booking by id
@router.get("/{booking_id}", response_model=BookingDisplay)
def get_booking(booking_id: int,
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    check_booker(booking_id, current_user, db)    
    return bookings_controller.get_booking(db, booking_id, current_user)

# Update a booking by id
@router.put("/{booking_id}", response_model= BookingDisplay)
def update_booking(booking_id: int,
                   request: BookingQuery,
                   db: Session = Depends(get_db),
                   current_user: DbUser = Depends(get_current_user)):
    check_booker(booking_id, current_user, db)
    return bookings_controller.update_booking(db, booking_id, request)

# delete a booking by id 
@router.delete("/{booking_id}")
def delete_booking(booking_id: int,
                   db: Session = Depends(get_db),
                   current_user: DbUser = Depends(get_current_user)):
    check_booker(booking_id, current_user, db)
    return bookings_controller.delete_booking(db, booking_id)

