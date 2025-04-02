from sqlalchemy.orm.session import Session
from schemas.vehicles_schema import VehicleBase
from db.models import db_vehicle
from fastapi import HTTPException, status



def create_vehicle (db:Session, request: VehicleBase ): 
    new_vehicle = db_vehicle(
        plate = request.plate,
        brand = request.brand,
        model = request.model,
        year = request.year,
        fuel_type = request.fuel_type,
        total_person = request.total_person,
        is_commercial = request.is_commercial,
        room_size = request.room_size,
        is_automatic = request.is_automatic,
        include_listing = request.include_listing,
        owner_id = request.owner_id
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle



def get_all_vehicles(db: Session):
     return db.query(db_vehicle).all()



def get_vehicle(db:Session, vehicle_id:int):
      req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
      if not req_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested vehicle with id {vehicle_id} is not found')
      return req_vehicle


def update_vehicle(db:Session, vehicle_id:int, request:VehicleBase):
     req_vehicle= db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
     if not req_vehicle:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Requested vehicle with id {vehicle_id} is not found')
     else:
         req_vehicle.vehicle_id = vehicle_id
         req_vehicle.plate = request.plate
         req_vehicle.brand = request.brand
         req_vehicle.model = request.model
         req_vehicle.year = request.year
         req_vehicle.fuel_type = request.fuel_type
         req_vehicle.total_person = request.total_person
         req_vehicle.is_commercial = request.is_commercial
         req_vehicle.room_size = request.room_size
         req_vehicle.is_automatic = request.is_automatic
         req_vehicle.include_listing = request.include_listing
         req_vehicle.owner_id = request.owner_id
     db.commit()
     db.refresh(req_vehicle)
     return req_vehicle

def delete_vehicle(db:Session, vehicle_id:int):
    req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
    if not req_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested vehicle with id {vehicle_id } is not found")
    db.delete(req_vehicle)
    db.commit()
    return f"Requested vehicle with id {vehicle_id} is deleted"




