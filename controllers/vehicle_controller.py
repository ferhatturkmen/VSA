from sqlalchemy.orm.session import Session
from schemas.vehicle_schema import VehicleBase
from db.models import db_vehicle

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
     return db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()

def update_vehicle(db:Session, vehicle_id:int, request:VehicleBase):
     vehicle= db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id)
     vehicle.update({
          db_vehicle.plate: request.plate, 
          db_vehicle.brand:request.brand, 
          db_vehicle.model :request.model,          
          db_vehicle.year : request.year, 
          db_vehicle.fuel_type : request.fuel_type, 
          db_vehicle.total_person : request.total_person, 
          db_vehicle.is_commercial : request.is_commercial, 
          db_vehicle.room_size : request.room_size, 
          db_vehicle.is_automatic : request.is_automatic, 
          db_vehicle.include_listing : request.include_listing, 
          db_vehicle.owner_id : request.owner_id
          })
     db.commit()
     return vehicle.first()

def delete_vehicle(db:Session, vehicle_id:int):
    vehicle = db.query(db_vehicle).filter(db_vehicle.vehicle_id == vehicle_id).first()
    db.delete(vehicle)
    db.commit()
    return "deleted"
#add exemption handling



