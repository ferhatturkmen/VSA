from fastapi import APIRouter, Depends, status
from schemas.vehicles_schema import VehicleBase, VehicleDisplay, VehicleQuery
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import vehicles_controller
from typing import List, Optional

router = APIRouter(
    prefix = "/vehicles",
    tags = ["vehicles"]
)
    

#create a new vehicle
@router.post("/new", response_model=VehicleDisplay, status_code=status.HTTP_201_CREATED)
def create_vehicle(request:VehicleBase, db : Session = Depends(get_db)):
    return vehicles_controller.create_vehicle(db, request)

#read all vehicles
@router.get("/all", response_model=List[VehicleDisplay])
def get_all_vehicles(db: Session = Depends(get_db),                   
                  query_params: VehicleQuery =  Depends()):
    req_db_query = vehicles_controller.get_all_vehicles(db, query_params=query_params)
    return req_db_query

'''#read all vehicles
@router.get("/", response_model=List[VehicleDisplay])
def get_all_vehicles(db: Session = Depends(get_db)):
    return vehicles_controller.get_all_vehicles(db)'''

#read vehicle by id 
@router.get("/{vehicle_id}", response_model=VehicleDisplay)
def get_vehicle(vehicle_id:int, db:Session=Depends(get_db)):
    return vehicles_controller.get_vehicle(db, vehicle_id)

'''#filter vehicles
@router.get("/filter/{brand}/{fuel_type}/{is_automatic}/{navigation}/{air_condition}")
def filter_vehicles(brand: Optional[str] = None, fuel_type: Optional[str] = None, is_automatic: Optional[bool] = None, navigation: Optional[bool] = None, air_condition: Optional[bool] = None, db: Session = Depends(get_db)):
    filtered_vehicles = vehicles_controller.get_filtered_vehicles(db, brand, fuel_type, is_automatic, navigation, air_condition)
    return filtered_vehicles'''

#update a vehicle by id                     #request changed to VehicleQuery 
@router.put("/{vehicle_id}/update", response_model=VehicleDisplay)
def update_vehicle(vehicle_id:int, request:VehicleQuery, db:Session=Depends(get_db)):
    return vehicles_controller.update_vehicle(db, vehicle_id, request)

#delete a vehicle by id 
@router.delete("/{vehicle_id}/delete")
def delete_vehicle(vehicle_id:int, db:Session=Depends(get_db)):
    return vehicles_controller.delete_vehicle(db, vehicle_id)



