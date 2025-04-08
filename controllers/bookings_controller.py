from sqlalchemy.orm import Session
from datetime import datetime,timezone,timedelta
from fastapi import HTTPException, status
from typing import List,Optional

from db.models import db_booking, db_payment, db_vehicle
from schemas.bookings_schema import BookingBase


# Create Booking

def create_booking(db: Session, request: BookingBase, current_user):
    # Booking_date as the rental start date
    start_date = request.booking_date
    # Calculate end date by adding total_days
    total_days = request.total_days
    end_date = start_date + timedelta(days=request.total_days)
    
    existing_booking = db.query(db_booking).filter(
        db_booking.renter_id == current_user.user_id,
        db_booking.rented_vehicle_id == request.rented_vehicle_id
    ).first()
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {current_user.user_id} has already booked vehicle {request.rented_vehicle_id}."
        ) 
    
    booking = db_booking(
        booking_date=start_date,
        created_at=datetime.now(timezone.utc),  # exact time of booking creation
        total_days=total_days,
        renter_id=current_user.user_id,
        rented_vehicle_id=request.rented_vehicle_id,
        
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # Create payment record (initial values)(Ask it to Ferhat abi)
    # payment = db_payment(
    #   booking_id=booking.booking_id,
    #   payment_amount=0.0,
    #   deposit_amount=0.0,
    #   is_pending=True,
    #   is_approved=False
    # )

    # db.add(payment)
    # db.commit()

    
    return booking


# View All Bookings

def get_all_bookings(db: Session,
                     current_user,
                     booking_date: Optional[str] = None,
                     is_cancelled: Optional[bool] = None,
                     rented_vehicle_id: Optional[int] = None,
                     total_days: Optional[int] = None):

    query = db.query(db_booking).filter(
        db_booking.renter_id == current_user.user_id
    )

    if booking_date:
        query = query.filter(db_booking.booking_date == booking_date)
    if is_cancelled is not None:
        query = query.filter(db_booking.is_cancelled == is_cancelled)
    if rented_vehicle_id:
        query = query.filter(db_booking.rented_vehicle_id == rented_vehicle_id)
    if total_days:
        query = query.filter(db_booking.total_days == total_days)

    return query.order_by(db_booking.booking_date.desc()).all()



#def get_all_bookings(db: Session, current_user) -> List[db_booking]:
#    bookings = db.query(db_booking).filter(
#        db_booking.renter_id == current_user.user_id
#    ).order_by(db_booking.booking_date.desc()).all()
#
#    return bookings
    


# View Single Booking

def get_booking(db: Session, booking_id: int, current_user):
    booking = db.query(db_booking).filter(
        db_booking.booking_id == booking_id,
        db_booking.renter_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


# Update Booking

def update_booking(db: Session, booking_id: int, request: BookingBase, current_user):
    booking = db.query(db_booking).filter_by(booking_id=booking_id, renter_id=current_user.user_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    
    start_date = booking.booking_date
    if start_date <= datetime.utcnow():
       raise HTTPException(
           status_code=400,
           detail="Cannot edit a booking that has already started"
        )
 
    
    booking.total_days = request.total_days
    booking.rented_vehicle_id = request.rented_vehicle_id
    db.commit()
    db.refresh(booking)
    
    return booking



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