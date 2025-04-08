from sqlalchemy.orm import Session

from fastapi import HTTPException, status, APIRouter, Depends
from schemas.properties_schema import VehiclePropertyCreate, VehiclePropertyOut
from db.database import get_db
from typing import List
from db.models import db_vehicle_property


# Function for creating a vehicle property
def create_vehicle_property(vehicle_properties: VehiclePropertyCreate, db: Session):
    vehicle_property = db_vehicle_property(**vehicle_properties.dict())
 
    db.add(vehicle_property)
    db.commit() 
    db.refresh(vehicle_property)   
    return vehicle_property

