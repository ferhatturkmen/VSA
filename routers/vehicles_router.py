from fastapi import APIRouter, Depends
from schemas.vehicle_schema import VehicleBase, VehicleDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import vehicle_controller
from typing import List

router = APIRouter(
    prefix = "/vehicle",
    tags = ["vehicle"]
)
    

#create a new user
@router.post("/", response_model=VehicleDisplay)
def create_vehicle(request:VehicleBase, db : Session = Depends(get_db)):
    return vehicle_controller.create_vehicle(db, request)

#read all users
@router.get("/", response_model=List[VehicleDisplay])
def get_all_vehicles(db: Session = Depends(get_db)):
    return vehicle_controller.get_all_vehicles(db)

#read user by id 
@router.get("/{vehicle_id}", response_model=VehicleDisplay)
def get_vehicle(vehicle_id:int, db:Session=Depends(get_db)):
    return vehicle_controller.get_vehicle(db, vehicle_id)

#update a user by id 
@router.put("/{vehicle_id}/update", response_model=VehicleDisplay)
def update_vehicle(vehicle_id:int, request:VehicleBase, db:Session=Depends(get_db)):
    return vehicle_controller.update_vehicle(db, vehicle_id, request)

#delete a user by id 
@router.delete("/{vehicle_id}/delete")
def delete(vehicle_id:int, db:Session=Depends(get_db)):
    return vehicle_controller.delete_vehicle(db, vehicle_id)

