from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
from typing import List

from db.models import db_booking, db_payment, db_vehicle
from schemas.bookings_schema import BookingBase


# ---------------------------------------------------
# VSA-46: Create Booking
# ---------------------------------------------------
def create_booking(db: Session, request: BookingBase, current_user):
    if request.start_time >= request.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    if request.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Start time must be in the future")

    vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == request.rented_vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    overlap = db.query(db_booking).filter(
        db_booking.rented_vehicle_id == request.rented_vehicle_id,
        db_booking.cancelled_at.is_(None),
        db_booking.end_time > request.start_time,
        db_booking.start_time < request.end_time
    ).first()
    if overlap:
        raise HTTPException(status_code=409, detail="Vehicle is already booked during this time")

    total_days = (request.end_time - request.start_time).days or 1

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

    payment = db_payment(
        booking_id=booking.booking_id,
        payment_amount=0.0,
        deposit_amount=0.0,
        is_pending=True,
        is_approved=False
    )
    db.add(payment)
    db.commit()

    return booking


# ---------------------------------------------------
# VSA-48: View All Bookings
# ---------------------------------------------------
def get_all_bookings(db: Session, current_user) -> List[db_booking]:
    return db.query(db_booking).filter(db_booking.renter_id == current_user.user_id).all()


# ---------------------------------------------------
# VSA-48: View Single Booking
# ---------------------------------------------------
def get_booking(db: Session, booking_id: int, current_user):
    booking = db.query(db_booking).filter(
        db_booking.booking_id == booking_id,
        db_booking.renter_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


# ---------------------------------------------------
# VSA-47: Update Booking
# ---------------------------------------------------
def update_booking(db: Session, booking_id: int, request: BookingBase, current_user):
    booking = db.query(db_booking).filter(
        db_booking.booking_id == booking_id,
        db_booking.renter_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot edit a booking that has already started")

    overlap = db.query(db_booking).filter(
        db_booking.rented_vehicle_id == request.rented_vehicle_id,
        db_booking.booking_id != booking_id,
        db_booking.cancelled_at.is_(None),
        db_booking.end_time > request.start_time,
        db_booking.start_time < request.end_time
    ).first()
    if overlap:
        raise HTTPException(status_code=409, detail="Vehicle is already booked during this time")

    booking.start_time = request.start_time
    booking.end_time = request.end_time
    booking.total_days = (request.end_time - request.start_time).days or 1
    booking.rented_vehicle_id = request.rented_vehicle_id
    booking.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)
    return booking


# ---------------------------------------------------
# VSA-47: Cancel Booking
# ---------------------------------------------------
def cancel_booking(db: Session, booking_id: int, current_user):
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
    db.refresh(booking)

    return {"message": "Booking successfully cancelled"}