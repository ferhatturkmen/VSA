from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from db.database import get_db
from db.models import DbUser
from auth.oauth2 import get_current_user
from schemas.bookings_schema import BookingBase, BookingDisplay
from controllers import bookings_controller

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# ---------------------------------------------------
@router.post("/", response_model=BookingDisplay, status_code=status.HTTP_201_CREATED)
def create_booking(request: BookingBase,
                   db: Session = Depends(get_db),
                   current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.create_booking(db, request, current_user)



# ---------------------------------------------------
@router.get("/", response_model=List[BookingDisplay])
def get_all_bookings(db: Session = Depends(get_db),
                     current_user: DbUser = Depends(get_current_user),
                     booking_date: Optional[str] = Query(None),
                     is_cancelled: Optional[bool] = Query(None),
                     rented_vehicle_id: Optional[int] = Query(None),
                     total_days: Optional[int] = Query(None)
                     ):
    return bookings_controller.get_all_bookings(
        db=db, 
        current_user=current_user,
        booking_date=booking_date,
        is_cancelled=is_cancelled,
        rented_vehicle_id=rented_vehicle_id,
        total_days=total_days
    )


# ---------------------------------------------------
@router.get("/{booking_id}", response_model=BookingDisplay)
def get_booking(booking_id: int,
                db: Session = Depends(get_db),
                current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.get_booking(db, booking_id, current_user)



# ---------------------------------------------------
@router.put("/{booking_id}", response_model=BookingDisplay)
def update_booking(booking_id: int,
                   request: BookingBase,
                   db: Session = Depends(get_db),
                   current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.update_booking(db, booking_id, request, current_user)



# ---------------------------------------------------
@router.patch("/{booking_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_booking(booking_id: int,
                   db: Session = Depends(get_db),
                   current_user: DbUser = Depends(get_current_user)):
    return bookings_controller.cancel_booking(db, booking_id, current_user)