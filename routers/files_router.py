from fastapi import APIRouter, Depends, File, UploadFile
from schemas.files_schema import VehicleImageDisplay
from schemas.users_schema import UserBase
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import files_controller 
from typing import List
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix = "/files",
    tags = ["files"]
)


#add vehicle image
@router.post("/{vehicle_id}/upload_images")
def upload_vehicle_images(vehicle_id:int, current_user:UserBase=Depends(get_current_user), files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
     image_paths = files_controller.upload_vehicle_images (db, vehicle_id, files)
     return {"image_paths": image_paths}


#get images by vehicle id
@router.get("/{vehicle_id}/images", response_model=List[VehicleImageDisplay])
def get_vehicle_images(vehicle_id:int, db:Session=Depends(get_db)):
    return files_controller.get_images_by_car(db, vehicle_id)


#delete vehicle image
@router.delete("/{vehicle_id}/delete_images")
def delete_vehicle_image(image_id:int, current_user:UserBase=Depends(get_current_user), db: Session = Depends(get_db)):
  return files_controller.delete_image(db, image_id)