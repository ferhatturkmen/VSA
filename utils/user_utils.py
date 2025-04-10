from schemas.users_schema import CurrentUserDisplay
from fastapi import HTTPException, status
from db.models import db_vehicle, db_booking, db_payment, db_review
from sqlalchemy.orm import Session

#Function to check if the user is authorized to access admin endpoints
def check_admin(current_user:CurrentUserDisplay):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access.")
        
# Function to check if the user is authorized to access user endpoints
def check_user(user_id:int, current_user:CurrentUserDisplay):
  if user_id != current_user.user_id and not current_user.is_admin:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this user.")

# Function to check if the user is authorized to access vehicle endpoints
def check_owner(vehicle_id:int, current_user:CurrentUserDisplay, db : Session):
  req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
  if not req_vehicle:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested vehicle is not found.")
  if req_vehicle.owner_id != current_user.user_id and not current_user.is_admin:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this vehicle.")

# Function to check if the user is authorized to access booking endpoints
def check_booker(booking_id: int, current_user: CurrentUserDisplay, db: Session):    
    req_booking = db.query(db_booking).filter(db_booking.booking_id == booking_id).first()  
    if not req_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested booking is not found.")  
    req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == req_booking.rented_vehicle_id).first()   
    if req_booking.renter_id != current_user.user_id and req_vehicle.owner_id != current_user.user_id and not current_user.is_admin:       
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this booking.") 


# Function to check if the user is authorized to access payment endpoints
def check_payer_reciever(payment_id: int, current_user: CurrentUserDisplay, db: Session):
  req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
  if not req_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested payment is not found.")
  req_booking = db.query(db_booking).filter(db_booking.booking_id == req_payment.booking_id).first()
  req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == req_booking.rented_vehicle_id).first()
  if req_booking.renter_id != current_user.user_id and req_vehicle.owner_id != current_user.user_id and not current_user.is_admin:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this payment.")
         
# Function to check if the user is authorized to access review endpoints
def check_reviewer(review_id: int, current_user: CurrentUserDisplay, db: Session):
  req_review = db.query(db_review).filter(db_review.review_id == review_id).first()
  if not req_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested review is not found.")
  req_booking = db.query(db_booking).filter(db_booking.booking_id == req_review.booking_id).first()
  req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == req_booking.rented_vehicle_id).first()
  if req_booking.renter_id != current_user.user_id and req_vehicle.owner_id != current_user.user_id and not current_user.is_admin:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this review.")
