from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from db.models import DbUser
from auth.oauth2 import get_current_user
#get_current_user function is missing in oauth2.py!!!
from schemas.bookings_schema import BookingBase, BookingDisplay
from controllers import bookings_controller

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# Create a new booking
@router.post("/", response_model=BookingDisplay, status_code=status.HTTP_201_CREATED)
def create_booking(request: BookingBase,
                   db: Session = Depends(get_db),
                   current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.create_booking(db, request, current_user)


# Get all bookings of the current user
@router.get("/", response_model=List[BookingDisplay])
def get_all_bookings(db: Session = Depends(get_db),
                     current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.get_all_bookings(db, current_user)


# Get booking by ID (only if it belongs to the current user)
@router.get("/{booking_id}", response_model=BookingDisplay)
def get_booking(booking_id: int,
                db: Session = Depends(get_db),
                current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.get_booking(db, booking_id, current_user)


# Cancel booking if it hasn't started yet
@router.put("/{booking_id}/cancel")
def cancel_booking(booking_id: int,
                   db: Session = Depends(get_db),
                   current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.cancel_booking(db, booking_id, current_user)