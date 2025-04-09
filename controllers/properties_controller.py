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


# Function for updating properties
def update_vehicle_property(property_id: int, vehicle_properties: VehiclePropertyCreate, db: Session):
    existing_property = db.query(db_vehicle_property).filter(db_vehicle_property.property_id == property_id).first()
    if not existing_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle property not found"
        )
    
    if vehicle_properties.daily_rate is not None:
        existing_property.daily_rate = vehicle_properties.daily_rate
    if vehicle_properties.location is not None:
        existing_property.location = vehicle_properties.location
    if vehicle_properties.unavailable_dates is not None:
        existing_property.unavailable_dates = vehicle_properties.unavailable_dates

    db.commit()
    db.refresh(existing_property)
    
    return existing_property




# Function for deleting properties
def delete_vehicle_property(property_id: int, db: Session):
    existing_property = db.query(db_vehicle_property).filter(db_vehicle_property.property_id == property_id).first()

    if not existing_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle property not found"
        )
     
    db.delete(existing_property)
    db.commit()
    
    return {"message": "Vehicle property deleted successfully"}