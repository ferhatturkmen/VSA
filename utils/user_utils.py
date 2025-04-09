from schemas.users_schema import UserBase, CurrentUserDisplay
from fastapi import HTTPException, status
from db.models import db_vehicle, db_booking, db_payment
from sqlalchemy.orm import Session



# Function to check if the user is authorized to access user endpoints
def check_user(user_id:int, current_user:UserBase):
  if user_id != current_user.user_id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this user.")

# Function to check if the user is authorized to access vehicle endpoints
def check_owner(vehicle_id:int, current_user:UserBase, db : Session):
  req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
  if req_vehicle.owner_id != current_user.user_id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this vehicle.")

# Function to check if the user is authorized to access booking endpoints
def check_booker(booking_id: int, current_user: CurrentUserDisplay, db: Session):    
    req_booking = db.query(db_booking).filter(db_booking.booking_id == booking_id).first()    
    req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == req_booking.rented_vehicle_id).first()   
    if req_booking.renter_id != current_user.user_id and req_vehicle.owner_id != current_user.user_id:       
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this booking.") 


# Function to check if the user is authorized to access payment endpoints
def check_payer_reciever(payment_id: int, current_user: CurrentUserDisplay, db: Session):
  req_payment = db.query(db_payment).filter(db_payment.payment_id == payment_id).first()
  req_booking = db.query(db_booking).filter(db_booking.booking_id == req_payment.booking_id).first()
  req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == req_booking.rented_vehicle_id).first()
  if req_booking.renter_id != current_user.user_id and req_vehicle.owner_id != current_user.user_id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this payment.")
         
    