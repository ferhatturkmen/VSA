from fastapi import APIRouter, Depends
from schemas.properties_schema import VehiclePropertyCreate, VehiclePropertyOut
from sqlalchemy.orm import Session
from db.database import get_db
from typing import List
from db.models import db_vehicle_property



router = APIRouter(
    prefix = "/vehicles",
    tags = ["properties"]
)


@router.post("/vehicle-properties/", response_model=VehiclePropertyOut)
def creating_vehicle_property(vehicle_property: VehiclePropertyCreate, db: Session = Depends(get_db)):
    db_vehicle_property = db_vehicle_property(**vehicle_property.dict())
    db.add(db_vehicle_property)
    db.commit()
    db.refresh(db_vehicle_property)
    return db_vehicle_property

@router.get("/vehicle-properties/{vehicle_id}", response_model=List[VehiclePropertyOut])
def getting_vehicle_properties(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle_properties = db.query(db_vehicle_property).filter(db_vehicle_property.vehicle_id == vehicle_id).all()
    return vehicle_properties