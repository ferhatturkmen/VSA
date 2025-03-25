from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix = "/vehicle",
    tags = ["vehicle"]
)

class vehicle_model(BaseModel):
    vehicle_id:int
    plate:str
    brand:str
    model:str
    year: int
    type: str
    


class availibilty(BaseModel):
    pass

@router.post("/new")
def create_vehicle(vehicle:vehicle_model):
    return f"{vehicle}"




@router.get ("/{vehicle_id}")
def get_vehicle_info(vehicle_id:int):
    return {"message" : f"this will be vehicle information for {vehicle_id}"}

@router.post("/{vehicle_id}/availibility")
def set_unavailibity_vehicle(vehicle_id:int ):
    pass
