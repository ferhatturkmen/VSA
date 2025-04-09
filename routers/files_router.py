from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, File,  UploadFile, status
from schemas.files_schema import VehicleFileDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from controllers import files_controller 
from typing import List

router = APIRouter(
    prefix = "/files",
    tags = ["files"]
)

#add vehicle's file
@router.post("/{vehicle_id}/new")
def upload_file(vehicle_id:int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
     file_paths = files_controller.upload_vehicle_file(db, vehicle_id, files)
     return JSONResponse(
          status_code=201,
          content={"file's_paths": file_paths}
     )


#get files by vehicle id
@router.get("/{vehicle_id}/", response_model=List[VehicleFileDisplay])
def get_file(vehicle_id:int, db:Session=Depends(get_db)):
    return files_controller.get_files_by_car(db, vehicle_id)





#delete vehicle file
@router.delete("/{vehicle_id}/delete")
def delete_file(file_id:int, db: Session = Depends(get_db)):
  
 return files_controller.delete_file(db, file_id)

