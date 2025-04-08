from sqlalchemy.orm.session import Session
from schemas.vehicles_schema import VehicleBase, VehicleQuery
from db.models import db_vehicle
from fastapi import HTTPException, status, Query
from typing import List, Optional


def create_vehicle (db:Session, request: VehicleBase ): 
    existing_vehicle = db.query(db_vehicle).filter(db_vehicle.plate == request.plate).first()
    if existing_vehicle:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"A vehicle with the plate {request.plate} already exists.")
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

def get_all_vehicles(db: Session, query_params: Optional[VehicleQuery] ):
    req_db_query = db.query(db_vehicle)
    if query_params:
        if query_params.plate:
            req_db_query = req_db_query.filter(db_vehicle.plate == query_params.plate)
        if query_params.brand:
            req_db_query = req_db_query.filter(db_vehicle.brand == query_params.brand)
        if query_params.model:
            req_db_query = req_db_query.filter(db_vehicle.model == query_params.model)
        if query_params.year:
            req_db_query = req_db_query.filter(db_vehicle.year == query_params.year)
        if query_params.fuel_type:
            req_db_query = req_db_query.filter(db_vehicle.fuel_type == query_params.fuel_type)
        if query_params.total_person:
            req_db_query = req_db_query.filter(db_vehicle.total_person == query_params.total_person)
        if query_params.is_commercial is not None:
            req_db_query = req_db_query.filter(db_vehicle.is_commercial == query_params.is_commercial)
        if query_params.room_size:
            req_db_query = req_db_query.filter(db_vehicle.room_size == query_params.room_size)
        if query_params.is_automatic is not None:
            req_db_query = req_db_query.filter(db_vehicle.is_automatic == query_params.is_automatic)
        if query_params.navigation is not None:
            req_db_query = req_db_query.filter(db_vehicle.navigation == query_params.navigation)
        if query_params.air_condition is not None:
            req_db_query = req_db_query.filter(db_vehicle.air_condition == query_params.air_condition)

    return req_db_query.all()





'''def get_all_vehicles(db: Session):
     return db.query(db_vehicle).all()'''



def get_vehicle(db:Session, vehicle_id:int):
      req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
      if not req_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Requested vehicle with id {vehicle_id} is not found')
      return req_vehicle

def update_vehicle(db: Session, vehicle_id: int, request: VehicleQuery):
    req_vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
    if not req_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested vehicle with id {vehicle_id} is not found")
        
    else:        
        if request.plate is not None:
            req_vehicle.plate = request.plate
        if request.brand is not None:
            req_vehicle.brand = request.brand
        if request.model is not None:
            req_vehicle.model = request.model
        if request.year is not None:
            req_vehicle.year = request.year
        if request.fuel_type is not None:
            req_vehicle.fuel_type = request.fuel_type
        if request.total_person is not None:
            req_vehicle.total_person = request.total_person
        if request.is_commercial is not None:
            req_vehicle.is_commercial = request.is_commercial
        if request.room_size is not None:
            req_vehicle.room_size = request.room_size
        if request.is_automatic is not None:
            req_vehicle.is_automatic = request.is_automatic
        if request.navigation is not None:
            req_vehicle.navigation = request.navigation
        if request.air_condition is not None:
            req_vehicle.air_condition = request.air_condition
        if request.include_listing is not None:
            req_vehicle.include_listing = request.include_listing
        if request.owner_id is not None:
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




