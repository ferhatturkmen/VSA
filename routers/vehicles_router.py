from fastapi import APIRouter, Depends, File, UploadFile
from schemas.vehicles_schema import VehicleBase, VehicleDisplay, VehicleImageDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import vehicles_controller
from typing import List

router = APIRouter(
    prefix = "/vehicles",
    tags = ["vehicles"]
)
    

#create a new vehicle
@router.post("/", response_model=VehicleDisplay)
def create_vehicle(request:VehicleBase, db : Session = Depends(get_db)):
    return vehicles_controller.create_vehicle(db, request)

#read all vehicles
@router.get("/", response_model=List[VehicleDisplay])
def get_all_vehicles(db: Session = Depends(get_db)):
    return vehicles_controller.get_all_vehicles(db)

#read vehicle by id 
@router.get("/{vehicle_id}", response_model=VehicleDisplay)
def get_vehicle(vehicle_id:int, db:Session=Depends(get_db)):
    return vehicles_controller.get_vehicle(db, vehicle_id)

#update a vehicle by id 
@router.put("/{vehicle_id}/update", response_model=VehicleDisplay)
def update_vehicle(vehicle_id:int, request:VehicleBase, db:Session=Depends(get_db)):
    return vehicles_controller.update_vehicle(db, vehicle_id, request)

#delete a vehicle by id 
@router.delete("/{vehicle_id}/delete")
def delete_vehicle(vehicle_id:int, db:Session=Depends(get_db)):
    return vehicles_controller.delete_vehicle(db, vehicle_id)


