from fastapi import APIRouter, Depends, File, UploadFile
from schemas.files_schema import VehicleImageDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import files_controller 
from typing import List

router = APIRouter(
    prefix = "/files",
    tags = ["files"]
)


#get images by vehicle id
@router.get("/{vehicle_id}/images", response_model=List[VehicleImageDisplay])
def getting_vehicle_images(vehicle_id:int, db:Session=Depends(get_db)):
    return files_controller.get_images_by_car(db, vehicle_id)


#add vehicle image
@router.post("/{vehicle_id}/upload_images")
def uploading_vehicle_images(vehicle_id:int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
     image_paths = files_controller.upload_vehicle_images (db, vehicle_id, files)
     return {"image_paths": image_paths}



#delete vehicle image
@router.delete("/{vehicle_id}/delete_images")
def deleting_vehicle_image(image_id:int, db: Session = Depends(get_db)):
  return files_controller.delete_image(db, image_id)