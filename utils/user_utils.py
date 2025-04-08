from schemas.users_schema import UserBase
from fastapi import HTTPException
from db.models import db_vehicle
from sqlalchemy.orm import Session

# Function to check if the user is authorized to access user endpoints
def check_user(user_id:int, current_user:UserBase):
  if user_id != current_user.user_id:
       raise HTTPException(status_code=403, detail="You are not authorized to access this user.")

# Function to check if the user is authorized to access vehicle endpoints
def check_owner(vehicle_id:int, current_user:UserBase, db : Session):
  req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
  if req_vehicle.owner_id != current_user.user_id:
       raise HTTPException(status_code=403, detail="You are not authorized to access this vehicle.")