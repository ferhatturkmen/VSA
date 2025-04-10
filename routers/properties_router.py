from fastapi import APIRouter, Depends
from schemas.properties_schema import VehiclePropertyCreate, VehiclePropertyOut, VehiclePropertyEditing
from sqlalchemy.orm import Session
from db.database import get_db
from typing import List
#from db.models import db_vehicle_property
from controllers.properties_controller import create_vehicle_property, update_vehicle_property, delete_vehicle_property


router = APIRouter(
    prefix = "/vehicles",
    tags = ["properties"]
)


# @router.post("/vehicle-properties/", response_model=VehiclePropertyOut)
# def creating_vehicle_property(vehicle_properties: VehiclePropertyCreate, db: Session = Depends(get_db)):
#     return create_vehicle_property(vehicle_properties, db)


# @router.get("/vehicle-properties/{vehicle_id}", response_model=List[VehiclePropertyOut])
# def getting_vehicle_properties(vehicle_id: int, db: Session = Depends(get_db)):
#     vehicle_properties = db.query(db_vehicle_property).filter(db_vehicle_property.vehicle_id == vehicle_id).all()
#     return vehicle_properties


# @router.put("/vehicle-properties/{property_id}", response_model=VehiclePropertyOut)
# def editing_vehicle_property(property_id: int, vehicle_properties: VehiclePropertyEditing, db: Session = Depends(get_db)):
#     return update_vehicle_property(property_id, vehicle_properties, db)


# @router.delete("/vehicle-properties/{property_id}")
# def deleting_vehicle_property(property_id: int, db: Session = Depends(get_db)):
#     return delete_vehicle_property(property_id, db)