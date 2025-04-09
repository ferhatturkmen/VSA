#from fastapi.responses import JSONResponse
from schemas.users_schema import UserBase
from fastapi import APIRouter, Depends, File,  UploadFile, status
from schemas.files_schema import VehicleFileDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import files_controller 
from typing import List
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix = "/files",
    tags = ["files"]
)

#add vehicle's file
@router.post("/{vehicle_id}/new")
def upload_file(vehicle_id:int, current_user:UserBase=Depends(get_current_user), files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
     
     #file_paths = files_controller.upload_vehicle_file(db, vehicle_id, files)
     #return {"image_paths": file_paths}
     return files_controller.upload_vehicle_file(db, vehicle_id, files)


#get files by vehicle id
@router.get("/{vehicle_id}/", response_model=List[VehicleFileDisplay])
def get_file(vehicle_id:int, db:Session=Depends(get_db)):
    return files_controller.get_files_by_car(db, vehicle_id)





#delete vehicle image
@router.delete("/{vehicle_id}/delete_images")
def delete_vehicle_image(image_id:int, current_user:UserBase=Depends(get_current_user), db: Session = Depends(get_db)):
  return files_controller.delete_image(db, image_id)