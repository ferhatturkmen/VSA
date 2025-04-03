from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status

from db.models import db_booking, db_payment, db_vehicle
from schemas.bookings_schema import BookingBase
from typing import List

def create_booking(db: Session, request: BookingBase, current_user):
    """
    Create a new booking if the vehicle is available and time is valid.
    Also creates a related payment record (initially pending).
    """

    # Validate time logic
    if request.start_time >= request.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    if request.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Start time must be in the future")

    # Validate vehicle existence
    vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == request.rented_vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Check availability (no overlapping bookings)
    overlap = db.query(db_booking).filter(
        db_booking.rented_vehicle_id == request.rented_vehicle_id,
        db_booking.cancelled_at == None,
        db_booking.end_time > request.start_time,
        db_booking.start_time < request.end_time
    ).first()

    if overlap:
        raise HTTPException(status_code=409, detail="Vehicle is already booked during this time")

    # Calculate total days
    total_days = (request.end_time - request.start_time).days
    if total_days == 0:
        total_days = 1  # minimum chargeable day

    # Create booking
    booking = db_booking(
        booking_date=datetime.utcnow(),
        start_time=request.start_time,
        end_time=request.end_time,
        total_days=total_days,
        renter_id=current_user.user_id,
        rented_vehicle_id=request.rented_vehicle_id,
        created_at=datetime.utcnow()
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # Create payment (placeholder logic)
    payment = db_payment(
        booking_id=booking.booking_id,
        payment_amount=0.0,  # Will be calculated later based on rate
        deposit_amount=0.0,
        is_pending=True,
        is_approved=False
    )
    db.add(payment)
    db.commit()

    return booking


def get_all_bookings(db: Session, current_user) -> List[db_booking]:
    """
    Returns all bookings of the current user (renter).
    """
    return db.query(db_booking).filter(db_booking.renter_id == current_user.user_id).all()


def get_booking(db: Session, booking_id: int, current_user):
    """
    Return a single booking by ID if it belongs to the current user.
    """
    booking = db.query(db_booking).filter(
        db_booking.booking_id == booking_id,
        db_booking.renter_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


def cancel_booking(db: Session, booking_id: int, current_user):
    """
    Cancel a booking if it belongs to the user and hasn't started yet.
    """
    booking = db.query(db_booking).filter(
        db_booking.booking_id == booking_id,
        db_booking.renter_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot cancel a booking that has already started")

    booking.is_cancelled = True
    booking.cancelled_at = datetime.utcnow()
    booking.cancellation_type = "user"
    db.commit()

    return {"message": "Booking successfully cancelled."}