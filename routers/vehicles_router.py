from fastapi import APIRouter, Depends
from schemas.vehicles_schema import VehicleBase, VehicleDisplay, VehicleImageDisplay, VehicleQuery
from schemas.users_schema import UserBase
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import vehicles_controller
from typing import List, Optional
from auth.oauth2 import oauth2_schema
from auth.oauth2 import get_current_user  
from utils.user_utils import check_owner  

router = APIRouter(
    prefix = "/vehicle",
    tags = ["vehicle"]
)
    

#create a new vehicle
@router.post("/", response_model=VehicleDisplay)
def create_vehicle(request:VehicleBase, 
                   current_user:UserBase=Depends(get_current_user), 
                   db : Session = Depends(get_db)):
    return vehicles_controller.create_vehicle(db, request)

#read all vehicles
@router.get("/all", response_model=List[VehicleDisplay])
def get_all_vehicles(db: Session = Depends(get_db),                   
                  query_params: VehicleQuery =  Depends()):
    req_db_query = vehicles_controller.get_all_vehicles(db, query_params=query_params)
    return req_db_query

#read vehicle by id 
@router.get("/{vehicle_id}", response_model=VehicleDisplay)
def get_vehicle(vehicle_id:int, 
                current_user:UserBase=Depends(get_current_user),  
                db:Session=Depends(get_db)):
    check_owner(vehicle_id, current_user, db)
    return vehicles_controller.get_vehicle(db, vehicle_id)


#update a vehicle by id                     #request changed to VehicleQuery 
@router.put("/{vehicle_id}/update", response_model=VehicleDisplay)
def update_vehicle(vehicle_id:int, 
                   request:VehicleQuery, 
                   current_user:UserBase=Depends(get_current_user), 
                   db:Session=Depends(get_db)):
    check_owner(vehicle_id, current_user, db)
    return vehicles_controller.update_vehicle(db, vehicle_id, request)

#delete a vehicle by id 
@router.delete("/{vehicle_id}/delete")
def delete_vehicle(vehicle_id:int, 
                   current_user:UserBase=Depends(get_current_user), 
                   db:Session=Depends(get_db)):
    check_owner(vehicle_id, current_user, db)
    return vehicles_controller.delete_vehicle(db, vehicle_id)



