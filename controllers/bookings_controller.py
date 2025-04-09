from sqlalchemy.orm import Session
from datetime import datetime,timezone,timedelta
from fastapi import HTTPException, status
from typing import List,Optional

from db.models import db_booking, db_payment, db_vehicle
from schemas.bookings_schema import BookingBase, BookingQuery
import pytz


# Create Booking

def create_booking(db: Session, request: BookingBase, current_user):
    
   # end_date = start_date + timedelta(days=request.total_days)
    
    '''existing_booking = db.query(db_booking).filter(
        db_booking.renter_id == current_user.user_id,
        db_booking.rented_vehicle_id == request.rented_vehicle_id
    ).first()
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {current_user.user_id} has already booked vehicle {request.rented_vehicle_id}."
        )''' 
    
    new_booking = db_booking(
        rented_vehicle_id=request.rented_vehicle_id,
        renter_id=current_user.user_id,
        start_date_time=request.start_date_time,
        end_date_time=request.end_date_time,
        is_delivered_up=False,
        damage_report="",
        is_report_approved=False,
        approved_at=None,
        is_cancelled=False,
        cancelled_at=None,
        created_at=datetime.now(timezone.utc)
        )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)    
    return new_booking


# View All Bookings

def get_all_bookings(db: Session,
                     query_params: Optional[BookingQuery] 
                     ):
    req_db_query = db.query(db_booking)
    if query_params:
        if query_params.booking_id:
            req_db_query = req_db_query.filter(db_booking.booking_id == query_params.booking_id)
        if query_params.rented_vehicle_id:
            req_db_query = req_db_query.filter(db_booking.rented_vehicle_id == query_params.rented_vehicle_id)
        if query_params.renter_id:
            req_db_query = req_db_query.filter(db_booking.renter_id == query_params.renter_id)
        if query_params.start_date_time:
            req_db_query = req_db_query.filter(db_booking.start_date_time == query_params.start_date_time)
        if query_params.end_date_time:
            req_db_query = req_db_query.filter(db_booking.end_date_time == query_params.end_date_time)
        if query_params.created_at:
            req_db_query = req_db_query.filter(db_booking.created_at == query_params.created_at)
        if query_params.is_delivered_up is not None:
            req_db_query = req_db_query.filter(db_booking.is_delivered_up == query_params.is_delivered_up)
        if query_params.damage_report:
            req_db_query = req_db_query.filter(db_booking.damage_report == query_params.damage_report)
        if query_params.is_report_approved is not None:
            req_db_query = req_db_query.filter(db_booking.is_report_approved == query_params.is_report_approved)
        if query_params.approved_at:
            req_db_query = req_db_query.filter(db_booking.approved_at == query_params.approved_at)
        if query_params.is_cancelled is not None:
            req_db_query = req_db_query.filter(db_booking.is_cancelled == query_params.is_cancelled)
        if query_params.cancelled_at:
            req_db_query = req_db_query.filter(db_booking.cancelled_at == query_params.cancelled_at)
    
    return req_db_query.all()


# Read a booking 

def get_booking(db: Session, booking_id: int, current_user):
    req_booking = db.query(db_booking).filter(db_booking.booking_id == booking_id, db_booking.renter_id == current_user.user_id).first()
    if not req_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Requested booking with id {booking_id} is not found')
    return req_booking

# Update Booking

def update_booking(db: Session, booking_id: int, request: BookingQuery):
    req_booking = db.query(db_booking).filter(db_booking.booking_id == booking_id).first()
    if not req_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested booking with id {booking_id} is not found.")
    if request.start_date_time <= datetime.now(pytz.timezone('Europe/Amsterdam')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot edit a booking that has already started")
    
    if request.booking_id is not None:
        req_booking.booking_id = request.booking_id
    if request.rented_vehicle_id is not None:
        req_booking.rented_vehicle_id = request.rented_vehicle_id
    if request.renter_id is not None:
        req_booking.renter = request.renter_id
    if request.start_date_time is not None:
        req_booking.start_date_time = request.start_date_time
    if request.end_date_time is not None:
        req_booking.end_date_time = request.end_date_time
    if request.is_delivered_up is not None:
        req_booking.is_delivered_up = request.is_delivered_up
    if request.damage_report is not None:
        req_booking.damage_report = request.damage_report
    if request.is_report_approved is not None:
        req_booking.is_report_approved = request.is_report_approved
    if request.approved_at is not None:
        req_booking.approved_at = request.approved_at
    if request.is_cancelled is not None:
        req_booking.is_cancelled = request.is_cancelled
    if request.cancelled_at is not None:
        req_booking.cancelled_at = request.cancelled_at
      
    db.commit()
    db.refresh(req_booking)
    return req_booking

#Delete a booking
def delete_booking(db: Session, booking_id: int, ):
    req_booking = db.query(db_booking).filter(db_booking.booking_id == booking_id).first()
    if not req_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested booking with id {booking_id} is not found.")
    db.delete(req_booking)
    db.commit()
    return f"Requested booking with id {booking_id} deleted."



# Cancel Booking

def cancel_booking(db: Session, booking_id: int, current_user):
    booking = db.query(db_booking).filter(
        db_booking.booking_id == booking_id,
        db_booking.renter_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    start_date = booking.booking_date
    if start_date <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel a booking that has already started"
        )
    
    booking.is_cancelled = True
    booking.cancelled_at = datetime.utcnow()
    booking.cancellation_type = "user"
    db.commit()
    db.refresh(booking)

    return {"message": "Booking successfully cancelled"}